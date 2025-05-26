from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from backend.models import *
from django.http import JsonResponse
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from backend.utils import learn

# Create your views here.
@login_required
def homepage(request):
    if request.method == 'POST':
        try:
            form_type = request.POST.get("form_type")

            if form_type == "salesForm":
                return addSales(request)
            elif form_type == "addProductForm":
                return addProduct(request)
            elif form_type == "orderForm":
                return addOrder(request)
            elif form_type == "stockForm":
                return addStock(request)
        except Exception as e:
            print(f"Unexpected Error: {e}") 
    else:
        productName = "No Product Name"

    return render(request, 'home/home.html')

def productFetch(request):
    product = request.POST.get("product")
    productObject = Product.objects.get(product_name = product)
    stockAmount = Stock.objects.filter(product_id = productObject).latest("stock_changed_date")
    print(stockAmount)
    return JsonResponse({"product": stockAmount.stock_amount }, safe=False)

def addProduct(request):
    if request.method == "POST":
        product_name = request.POST.get("productName")
        product_description = request.POST.get("productDescription")
        product_units = request.POST.get("productUnits")
        product_category = request.POST.get("productCategory")
        product_cost = request.POST.get("productCost")
        product_price = request.POST.get("productPrice")
        product_stock = request.POST.get("productStock")

        # Fetch the related objects
        category = Category.objects.get(category_name=product_category)
        unit = Unit.objects.get(unit_of_measurement=product_units)
        # Create the product
        Product.objects.create(
            product_name=product_name,
            product_description=product_description,
            category_id=category,
            unit_id=unit,
            product_cost=product_cost,
            product_price=product_price
        )

        product_sale_reference_name = Product.objects.get(product_name=product_name)

        Stock.objects.create(
            product_id = product_sale_reference_name,
            stock_amount = product_stock
        )

        return JsonResponse({"product": product_name})

def addOrder(request):
    #Adds order to the models and records Transaction
    product_order_name =request.POST.get('productOrderName')
    product_order_quantity = request.POST.get("productOrderQuantity")
    supplier_name = request.POST.get("supplierName")
    product_order_price = request.POST.get("productCreationPrice")
    order_expected_date= request.POST.get("orderExpectedDate")
    print(order_expected_date)
    
    order_date_object = datetime.strptime(order_expected_date, '%Y-%m-%d')
    formatted_date = order_date_object.strftime('%Y-%m-%d')
    print(order_date_object)
    print(formatted_date)
    
    
    product_order_ref_name = Product.objects.get(product_name=product_order_name)
    
    OrderItem.objects.create(
        product = product_order_ref_name,
        product_quantity = product_order_quantity,
        unit_price = product_order_price,
    )
    
    messages.success(request, "Your Order has been placed Successfully")
    success = True
    
    latest_cost = OrderItem.objects.filter(product_id=product_order_ref_name.product_id).latest('order_date')
    total_cost = latest_cost.total_price 
    
    Order.objects.create(
        order_number = "0",
        expected_date = formatted_date,
        order_status = "PENDING",
        order_quantity = 1,
        order_total_price = total_cost
    )
    
    order_id = OrderItem.objects.filter(product=product_order_ref_name).latest('order_item_id')
    
    Transactions.objects.create(
        product_id = product_order_ref_name,
        transaction_amount = total_cost,
        transaction_type = 'ORDER',
        order_id = order_id,
        transaction_payment_method = 'Mpesa'
    ) 
    
    stock_amt = Stock.objects.filter(product_id=product_order_ref_name.product_id).latest('stock_changed_date')
    new_stock_amt = stock_amt.stock_amount + int(product_order_quantity)
    print(new_stock_amt)
    Stock.objects.create(
        product_id = product_order_ref_name,
        stock_amount = new_stock_amt
    )
    stock_reference_name = Stock.objects.filter(product_id = product_order_ref_name.product_id).latest('stock_changed_date')
    

    
    backendData = {
        "product_name": product_order_name,
        'remaining_stock': stock_reference_name.stock_amount,
        'success': success
        }
    return render(request, 'home/home.html', backendData)


def addSales(request):
    # Records Sales and adds Transaction
    product_sale_name = request.POST.get('productSaleName')
    product_sale_quantity = request.POST.get("productSaleQuantity")  
    product_payment_method = request.POST.get("purchaseMethod")
    
    learn(product_sale_name)

    product_sale_reference_name = Product.objects.get(product_name=product_sale_name)
    stock_reference_name = Stock.objects.filter(product_id = product_sale_reference_name.product_id).latest('stock_changed_date')
    print(stock_reference_name.stock_amount)
    remaining_product = stock_reference_name.stock_amount - int(product_sale_quantity)
    
    if remaining_product < 0:
        print("Low on stock")
        messages.error(request, "You have low stock on the selected Product")
        success = False
        error = True
    else:
        error = False
        Stock.objects.create(
            product_id = product_sale_reference_name,
            stock_amount = remaining_product,
        )
        
        SalesItem.objects.create(
        product_id = product_sale_reference_name,
        product_quantity = product_sale_quantity
        )
        stock_reference_name = Stock.objects.filter(product_id = product_sale_reference_name.product_id).latest('stock_changed_date')
        
        
        latest_sale = SalesItem.objects.filter(product_id=product_sale_reference_name).latest('saleItem_id')
    
        total_cost = latest_sale.product_totalCost
    
        Transactions.objects.create(
            product_id = product_sale_reference_name,
            transaction_amount = total_cost,
            transaction_type = 'SALE',
            transaction_payment_method = product_payment_method
        )
        messages.success(request, "Sale done successfully")
        success = True

    backendData = {
        "product_name": product_sale_name,
        'remaining_stock': stock_reference_name.stock_amount,
        'error': error,
        'success': success
        }
    
    return render(request, 'home/home.html', backendData )  

def addStock(request):
    #The retailer can add the product to the database without a supplier
    product_stock_name = request.POST.get("productStockName")
    product_stock_quantity = request.POST.get("productStockQuantity")
    
    product_stock_ref_name = Product.objects.get(product_name=product_stock_name)

    stock_amt = Stock.objects.filter(product_id=product_stock_ref_name.product_id).latest("stock_changed_date")
    new_stock_amt = stock_amt.stock_amount + int(product_stock_quantity)
    Stock.objects.create(product_id=product_stock_ref_name, stock_amount=new_stock_amt)
    
    return render(request, 'home/home.html')


def dynamicData(request):
    product_name = request.GET.get("product_id")
    product_sale_reference_name = Product.objects.get(product_name=product_name)
    stock_reference_name = Stock.objects.filter(product_id = product_sale_reference_name.product_id).latest('stock_changed_date')
    print(stock_reference_name.stock_amount)
    print(product_sale_reference_name.unit_id)
    if product_sale_reference_name:
        return JsonResponse({
            "quantity": stock_reference_name.stock_amount,
            "unit": product_sale_reference_name.unit_id
        })
    
    return JsonResponse({"error": "Product not found"}, status=404)
