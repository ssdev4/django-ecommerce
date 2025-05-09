from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import Cart, CartItem
from products.models import Product
from django.views.generic import TemplateView
from django.contrib import messages

class AddToCartView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        # Handle quantity from form or default to 1
        quantity = int(request.POST.get('quantity', 1))

        # Check inventory
        if not hasattr(product, 'inventory') or product.inventory.stock < quantity:
            messages.error(request, "Item is not available in stock.")
            return redirect('products:product_detail', pk=pk)

        #create session if not already
        if not request.session.session_key:
            request.session.create()

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

        messages.success(request, "Item added to cart successfully!")
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

# Remove Item from Cart
class RemoveFromCartView(View):
    def post(self, request, pk):
        # Find the cart item to remove
        cart_item = get_object_or_404(CartItem, pk=pk)

        # Delete it
        cart_item.delete()

        return redirect('cart:cart_detail')

# Update Quantity in Cart

class UpdateQuantityView(View):
    def post(self, request, pk):
        # Get the cart item
        cart_item = get_object_or_404(CartItem, pk=pk)
        product = cart_item.product

        # Get the new quantity from the form
        new_quantity = int(request.POST.get('quantity', 1))

        # ✅ Validate stock before updating
        if not hasattr(product, 'inventory') or product.inventory.stock < new_quantity:
            messages.error(request, "Cannot add more than available stock.")
            return redirect('cart:cart_detail')  # or redirect to same page with message

        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        messages.success(request, "Updated cart successfully!")
        return redirect('cart:cart_detail')
