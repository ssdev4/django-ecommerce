from django.shortcuts import render
from checkout.models import Order
from django.contrib.auth.decorators import login_required

@login_required
def order_history(request):
    # Get orders for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders
    }

    return render(request, 'orders/order_history.html', context)
