from django.urls import path, include
from . import views

urlpatterns= [
    path('', views.frontend, name='frontend'),
    path('home', views.landingPage, name="landingPage"),
    path('downloadImage', views.downloadImage, name="downloadImage")
]