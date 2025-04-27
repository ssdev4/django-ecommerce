from celery import shared_task
from .email_service import send_order_confirmation_email
from ..models import Order

@shared_task
def send_order_confirmation_email_task(order_id):
    """
    This Celery task sends the order confirmation email asynchronously.
    """
    try:
        order = Order.objects.get(id=order_id)
        send_order_confirmation_email(order)
    except Order.DoesNotExist:
        # Handle the case where the order does not exist (e.g., log it)
        print(f"Order with ID {order_id} does not exist.")