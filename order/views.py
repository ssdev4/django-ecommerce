from django.shortcuts import render
from checkout.models import Order
from django.contrib.auth.decorators import login_required

# @login_required
def order_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    else:
        session_key = request.session.session_key
        orders = Order.objects.filter(session_key=session_key).order_by('-created_at')
    
    context = {
        'orders': orders
    }

    return render(request, 'orders/order_history.html', context)
