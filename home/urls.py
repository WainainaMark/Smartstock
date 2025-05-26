from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('dynamicData', views.dynamicData, name="dynamicData"),
    path('/addProduct', views.addProduct, name="addProduct"),
    path('/productFetch', views.productFetch, name="productFetch"),
    path('/learn', views.modelLearn, name="modelLearn")
]