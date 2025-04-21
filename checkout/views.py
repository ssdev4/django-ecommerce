from django.shortcuts import render, redirect
from django.views import View
from .forms import CheckoutForm
from .models import Order, OrderItem
from cart.models import Cart
from django.views.generic import TemplateView
from django.db.models import Q

class CheckoutView(View):
    def get(self, request):
        form = CheckoutForm()
        return render(request, 'checkout/checkout.html', {'form': form})

    def post(self, request):
        form = CheckoutForm(request.POST)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            else:
                order.session_key = request.session.session_key
            order.save()

            # Fetch the current cart
            # cart = Cart.objects.filter(
            #     Q(user=request.user) | Q(session_key=request.session.session_key)
            # ).first()

            # Fetch the current cart for logged-in or guest users
            if request.user.is_authenticated:
                # For logged-in users, retrieve cart by user
                cart = Cart.objects.filter(user=request.user).first()
            else:
                # For guest users, retrieve cart by session_key
                cart = Cart.objects.filter(session_key=request.session.session_key).first()

            if cart:
                for item in cart.items.all():
                    # Check stock before creating OrderItem
                    inventory = item.product.inventory
                    try:
                        inventory.update_stock(item.quantity)  # Reduce stock
                    except ValueError:
                        # Optional: handle out-of-stock error gracefully
                        # For now, just re-raise it to stop the checkout
                        raise

                    # Create the order item only if stock was reduced
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price
                    )
                # Clear the cart
                cart.items.all().delete()

            return redirect('checkout:order_success')

        return render(request, 'checkout/checkout.html', {'form': form})

class OrderSuccessView(TemplateView):
    template_name = 'checkout/success.html'
