import pandas as pd
from backend.models import *
from django.db import models
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import google.generativeai as genai

# pyright: reportPrivateImportUsage=false
genai.configure(api_key="AIzaSyBs14-UX4cSwNuCT-XeB9bRmQLgyx05uHQ")
AImodel = genai.GenerativeModel("gemini-2.0-flash")
def insertData(product_name: str):
    """
    The machine learns about the previous transactions of the object
    """
    print("The machine got " + product_name)
    product_sale_reference_name = Product.objects.get(product_name=product_name)
    transactions = Transactions.objects.filter(product_id = product_sale_reference_name)

    # Extract the values into separate lists
    types = []
    amounts = []

    for transaction in transactions:
        types.append(transaction.transaction_type)
        amounts.append(transaction.transaction_amount)

    # Make the data dictionary
    data = {
        "type": types,
        "amount": amounts
    }

    # Optional: convert to pandas DataFrame
    df = pd.DataFrame(data)

    # Encode 'type' (ORDER=0, SALE=1)
    df['type_encoded'] = df['type'].map({'ORDER': 0, 'SALE': 1})

    # Add a time index (assuming data is in chronological order)
    df['time_index'] = range(1, len(df) + 1)

    df.to_csv(f'{product_name}_transactions.csv')
    print("CSV saved using pandas! File: transactions.csv ✅")

def learn(product_name: str):
    print(f"🔍 Analyzing transactions for product: {product_name}")

    try:
        # Fetch product and transactions
        product = Product.objects.get(product_name=product_name)
        transactions = Transactions.objects.filter(product_id=product)

        if not transactions.exists():
            print("⚠️ No transactions found for this product!")
            return

        # Prepare data
        data = {
            "type": [t.transaction_type for t in transactions],
            "amount": [t.transaction_amount for t in transactions],
            "date": [t.transaction_date for t in transactions]  # Assuming you have a 'transaction_date' field
        }
        df = pd.DataFrame(data)

        # Save CSV
        filename = f'{product_name}_transactions.csv'
        df.to_csv(filename, index=False)
        print(f"💾 Saved transactions to: {filename}")

        # Filter only 'SALE' transactions for training
        df_sales = df[df['type'] == 'SALE'].copy()

        if df_sales.empty:
            print("⚠️ No SALE data to train on.")
            return

        # Add time index (assumes 'date' is in chronological order)
        df_sales['date'] = pd.to_datetime(df_sales['date'])
        df_sales = df_sales.sort_values('date')
        df_sales['time_index'] = range(1, len(df_sales) + 1)

        # Features (X) and target (y)
        X = df_sales[['time_index']]
        y = df_sales['amount']

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train regression model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Predict next 3 time steps
        next_indexes = np.array([[X['time_index'].max() + i] for i in range(1, 4)])
        forecast = model.predict(next_indexes)
        forecast = np.clip(forecast, 0, None)
        
        total_predicted = sum(forecast)

        print(f"📈 Next 3 predicted SALE amounts: {forecast}")
        print(f"🧮 Total predicted demand (next 3): {total_predicted:.2f}")
        response = AImodel.generate_content(f"Give me advice based on the predicted sale trend of the product {product_name} in one sentence: The predicted forecast data is like this {forecast.tolist()}")

        return {
            'product': product_name,
            'forecast': forecast.tolist(),
            'total_predicted': int(total_predicted),
            'response': response.text
        }

    except Product.DoesNotExist:
        print(f"❌ Product '{product_name}' not found!")
        return None


# sales = SalesItem.objects.all().values()
# df = pd.DataFrame(sales)