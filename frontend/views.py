from django.http import JsonResponse
from django.shortcuts import render
from backend.models import *
from django.core.files.base import ContentFile
import requests
import os, random
from urllib.parse import urlparse, unquote

# Create your views here.
def landingPage(request):
    return render(request, 'frontend/home.html')


def frontend(request):

    if request.method == "POST":
        try:
            form_type = request.POST.get("form_type")

            if form_type == "productAddForm":
                return addSales(request)
            elif form_type == "supplierAddForm":
                return addSupplier(request)
            # elif form_type == "orderForm":
            #     return addOrder(request)
            # elif form_type == "stockForm":
            #     return addStock(request)
        except Exception as e:
            print(f"Unexpected Error: {e}")
    else:
        productName = "No Product Name"

    return render(request, "frontend/frontend.html")

def addSales(request):
        productName = request.POST.get("productAdd")
        productUnit = request.POST.get("productUnit")
        productCategory = request.POST.get('productCategory')
        body_unicode = request.body.decode("utf-8")
        # data = json.loads(body_unicode)
        # description = data.get("description", "").strip()
        description = request.POST.get('description')
        productManufacturer = request.POST.get('manufacturer')
        productNewManufacturer = request.POST.get('manufacturerNew')
        productCost = request.POST.get('cost')
        productPrice = request.POST.get('price')
        productPhotoUrl = request.POST.get('photoUrl')
        productPhoto = request.FILES.get('fileInput')

        print(productName)
        print(productUnit)
        print(productCategory)
        print(description)
        print(productManufacturer)
        print(productNewManufacturer)
        print(productCost)
        print(productPrice)
        print(productPhotoUrl)
        print(productPhoto)

        category = Category.objects.get(category_name = productCategory)
        unit = Unit.objects.get(unit_of_measurement = productUnit)
        if(productNewManufacturer!=""):
            Manufacturer.objects.create(
                manufacturer_name = productNewManufacturer
            )
            manufacturer = Manufacturer.objects.get(manufacturer_name=productManufacturer)

        manufacturer = Manufacturer.objects.get(manufacturer_name = productManufacturer)

        product = Product.objects.create(
            product_name = productName,
            product_description = description,
            product_manufacturer = manufacturer,
            category_id = category,
            unit_id = unit,
            product_cost = productCost,
            product_price = productPrice,
            product_photo = productPhoto
        )

        if productPhotoUrl:
            response = requests.get(productPhotoUrl)

            if response.status_code == 200:
                response = requests.get(productPhotoUrl, stream=True)
                response.raise_for_status()
                parsed_url = urlparse(productPhotoUrl)
                filename = os.path.basename(parsed_url.path)
                filename = unquote(filename)

                product.product_photo.save(filename, ContentFile(response.content), save=True)

        elif productPhoto:
            product.product_photo.save(productPhoto.name, productPhoto, save=True)

        return render(request, 'frontend/frontend.html')


def addSupplier(request):
    print(request.POST)
    Supplier.objects.create(
        supplier_name = request.POST.get('supplierName'),
        supplier_title = request.POST.get('supplierTitle'),
        supplier_number = request.POST.get('supplierPhoneNumber'),
        supplier_location = request.POST.get('supplierLocation')
    )
    return render(request, 'frontend/frontend.html')


def chart_data(request):
    data = {
        "labels": ["January", "February", "March", "April", "May"],
        "values": [random.randint(10, 100) for _ in range(5)],
    }
    return JsonResponse(data)  # Returns JSON data for Chart.js


def graph_page(request):
    return render(request, "frontend/graph.html")
