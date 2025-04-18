from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import Cart, CartItem
from products.models import Product
from django.views.generic import TemplateView

class AddToCartView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        # Handle logged in user or session
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key or request.session.save()
            cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)

        # Add item or update quantity
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('products:product_detail', pk=pk)

class CartDetailView(TemplateView):
    template_name = 'cart/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
        else:
            session_key = self.request.session.session_key or self.request.session.save()
            cart = Cart.objects.filter(session_key=self.request.session.session_key).first()

        context['cart'] = cart
        return context
