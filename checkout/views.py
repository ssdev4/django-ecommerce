from django.shortcuts import render, redirect
from django.views import View
from .forms import CheckoutForm
from .models import Order, OrderItem
from cart.models import Cart
from django.views.generic import TemplateView

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
            order.save()

            # Fetch the current cart
            cart = Cart.objects.filter(user=request.user if request.user.is_authenticated else None,
                                       session_key=request.session.session_key).first()
            if cart:
                for item in cart.items.all():
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
