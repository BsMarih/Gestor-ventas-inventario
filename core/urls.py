from django.urls import path
from django.core.paginator import Paginator
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sales/', views.sales, name='sales'),
    path('inventory/', views.inventory, name='inventory'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path("create/", views.create_element, name="create_element"),
    path('ajax/get_types/', views.get_types, name='get_types'),
]