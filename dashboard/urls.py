from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/update/<int:product_id>/', views.update_inventory, name='update_inventory'),
]
