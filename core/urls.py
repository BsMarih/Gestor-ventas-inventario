from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sales/', views.sales, name='sales'),
    path('inventory/', views.inventory, name='inventory'),
]