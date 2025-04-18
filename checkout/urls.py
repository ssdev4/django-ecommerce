from django.urls import path
from .views import CheckoutView, OrderSuccessView

app_name = 'checkout'

urlpatterns = [
    path('', CheckoutView.as_view(), name='checkout'),
    path('success/', OrderSuccessView.as_view(), name='order_success'),
]
