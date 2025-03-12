from collections import defaultdict
from django.utils.timezone import localtime
from django.db.models import Sum
from backend.models import *


def backend_data(request):
    suppliers = Supplier.objects.all()
    products = Product.objects.all()
    categories = Category.objects.all()
    units = Unit.objects.all()
    total_product = Product.objects.count()
    user_logged_in = request.user
    paymentMethods = {"Mpesa": "mpesa", "Cash": "cash", "Loop": "loop"}

    today = localtime().date()
    full_total_cost = SalesItem.objects.aggregate(Sum("product_totalCost"))[
        "product_totalCost__sum"
    ]
    full_order_total_cost = OrderItem.objects.aggregate(Sum("total_price"))[
        "total_price__sum"
    ]
    # Total sales and orders today
    sales_by_type_today = (
        Transactions.objects.filter(transaction_date__startswith=today)
        .values("transaction_type")
        .annotate(total=Sum("transaction_amount"))
    )

    total_sales_today = sum(
        item["total"]
        for item in sales_by_type_today
        if item["transaction_type"] == "SALE"
    )
    total_order_today = sum(
        item["total"]
        for item in sales_by_type_today
        if item["transaction_type"] == "ORDER"
    )
    total_profit_today = total_sales_today - total_order_today

    # Weekly sales & order data
    from collections import defaultdict


    # Retrieve all transactions
    transactions = Transactions.objects.all()

    # Initialize default dictionary for daily totals
    daily_totals = defaultdict(lambda: {"sales": 0, "orders": 0})

    # List of all days of the week
    all_days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    # Aggregate sales and orders for all days, only if transactions exist
    for transaction in transactions:
        transaction_day = transaction.transaction_date.strftime("%A")  # "Monday", etc.
        if transaction_day in all_days:  # Valid day check
            if transaction.transaction_type == "SALE":
                daily_totals[transaction_day]["sales"] += transaction.transaction_amount
            elif transaction.transaction_type == "ORDER":
                daily_totals[transaction_day]["orders"] += transaction.transaction_amount

    # Calculate profits and store results for all days
    daily_results = {}
    for day in all_days:
        sales_total = daily_totals[day]["sales"]
        orders_total = daily_totals[day]["orders"]
        profit = sales_total - orders_total
        daily_results[day] = {
            "sales_total": sales_total,
            "orders_total": orders_total,
            "profit": profit,
        }

    
    return {
        "full_total_cost": full_total_cost,
        "full_order_total_cost": full_order_total_cost,
        "products": products,
        "suppliers": suppliers,
        "categories": categories,
        'total_product': total_product,
        "units": units,
        "paymentMethods": paymentMethods,
        "transactions": transactions,
        "user": user_logged_in,
        "total_sales_today": total_sales_today,
        "total_order_today": total_order_today,
        "total_profit": total_profit_today,
        "daily_results": daily_results
    }
