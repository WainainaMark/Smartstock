from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.frontend, name="frontend"),
    path("home", views.landingPage, name="landingPage"),
    path("chart-data/", views.chart_data, name="chart-data"),
    path("graph/", views.graph_page, name="graph-page"),
]
