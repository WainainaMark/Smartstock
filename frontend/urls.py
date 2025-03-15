from django.urls import path, include
from . import views

urlpatterns= [
    path('', views.frontend, name='frontend'),
    path('downloadImage', views.downloadImage, name="downloadImage")
]