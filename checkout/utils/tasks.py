from celery import shared_task
from .email_service import send_order_confirmation_email
from ..models import Order
from django.core.exceptions import ObjectDoesNotExist
from smtplib import SMTPException  # For mail sending errors

@shared_task(bind=True, max_retries=5, default_retry_delay=30)  # 5 retries, wait 30s by default
def send_order_confirmation_email_task(self, order_id):
    """
    Celery task: Sends order confirmation email asynchronously.
    Retries automatically on failure (order missing or email sending error).
    """
    try:
        order = Order.objects.get(id=order_id)
        send_order_confirmation_email(order)

    except (ObjectDoesNotExist, SMTPException) as exc:
        print(f"Unexpected error occurred sending order email: {exc}")
        countdown = 30 * self.request.retries
        raise self.retry(exc=exc, countdown=countdown)

    except Exception as e:
        # not recommended to retry on general exceptions rather should log it
        print(f"Unexpected error sending order email: {e}")
        # raise self.retry()
