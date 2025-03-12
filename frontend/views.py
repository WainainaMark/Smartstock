from django.shortcuts import render
from backend.models import Product, Category, Unit

# Create your views here.
def frontend(request):
    if request.method == "POST":
        # ProductAddForm
        product_name = request.POST.get('productAddName')
        product_photo = request.FILES.get('productPhoto')
        product_description = request.POST.get('productDescription')
        category_id = request.POST.get('productCategory')
        unit_id = request.POST.get('productUnit')
        product_cost = request.POST.get('productCost')
        product_price = request.POST.get('productCreationPrice')
        product_quantity = request.POST.get('productInitialQuantity')



        # Fetch the related objects
        category = Category.objects.get(category_name=category_id)
        unit = Unit.objects.get(unit_of_measurement=unit_id)
        # Create the product
        Product.objects.create(
            product_name=product_name,
            product_photo=product_photo,
            product_description=product_description,
            category_id=category,
            unit_id=unit,
            product_cost=product_cost,
            product_price=product_price,
            product_quantity=product_quantity
        )
        
    products = Product.objects.all()   
    categories = Category.objects.all()
    units= Unit.objects.all()
    
    backendData = {
        'products': products,
        'categories': categories,
        'units': units,
    } 
    
    
    return render(request, 'frontend/productAddForm.html', backendData)