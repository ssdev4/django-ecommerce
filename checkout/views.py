from django.shortcuts import render, redirect
from django.views import View
from .forms import CheckoutForm
from .models import Order, OrderItem
from cart.models import Cart
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib import messages
from .services.email_service import send_order_confirmation_email

class CheckoutView(View):
    def get(self, request):
        form = CheckoutForm()
        return render(request, 'checkout/checkout.html', {'form': form})

    def post(self, request):
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            else:
                order.session_key = request.session.session_key
            order.save()

            # Fetch cart
            if request.user.is_authenticated:
                cart = Cart.objects.filter(user=request.user).first()
            else:
                cart = Cart.objects.filter(session_key=request.session.session_key).first()

            if cart:
                for item in cart.items.all():
                    product = item.product

                    # Inventory check
                    if not hasattr(product, 'inventory') or product.inventory.stock < item.quantity:
                        messages.error(request, f"Insufficient stock for {product.name}")
                        form.add_error(None, f"Insufficient stock for {product.name}")
                        return render(request, 'checkout/checkout.html', {'form': form})

                for item in cart.items.all():
                    inventory = item.product.inventory
                    try:
                        inventory.update_stock(item.quantity)
                    except ValueError:
                        raise

                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price
                    )

                cart.items.all().delete()

                # Send Order Confirmation Email
                send_order_confirmation_email(order)

            return redirect('checkout:order_success')

        return render(request, 'checkout/checkout.html', {'form': form})

class OrderSuccessView(TemplateView):
    template_name = 'checkout/success.html'
