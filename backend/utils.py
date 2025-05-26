import pandas as pd
from backend.models import *
from django.db import models

def learn(product_name: str):
    """
    The model learns about the previous transactions of the object
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



print("CSV saved using pandas! File: transactions.csv ✅")
# sales = SalesItem.objects.all().values()
# df = pd.DataFrame(sales)
# df.to_csv('sales_data.csv')