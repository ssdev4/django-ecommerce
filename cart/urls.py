from django.urls import path
from .views import AddToCartView, CartDetailView, RemoveFromCartView, UpdateQuantityView

app_name = 'cart'

urlpatterns = [
    path('add/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:pk>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('update/<int:pk>/', UpdateQuantityView.as_view(), name='update_quantity'),
    path('', CartDetailView.as_view(), name='cart_detail'),
]
