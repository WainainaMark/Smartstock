from django.urls import path, include
from . import views

urlpatterns= [
    path('', views.signIn, name='signIn'),
    path('login', views.login, name='login'),
    path('terms', views.terms, name='terms'),
    path('privacy', views.privacy, name='privacy'),
    path('forgot', views.forgot, name='forgot'),
    path('verifyOTP', views.verifyOTP, name='verifyOTP'),
    path('reset', views.reset, name='reset'),
    path('home', include('home.urls'))
    
]