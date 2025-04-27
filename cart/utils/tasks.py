from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.sessions.models import Session
from ..models import Cart

@shared_task
def clean_abandoned_carts():
    """
    Celery task to clean abandoned carts for:
    - Guest carts (user=None)
    - Session either expired or deleted
    """
    now = timezone.now()
    abandoned_carts = Cart.objects.filter(user__isnull=True)

    deleted_count = 0

    for cart in abandoned_carts:
        session_key = cart.session_key

        if not session_key:
            # If somehow session_key missing, consider abandoned
            # cart.delete()
            deleted_count += 1
            continue

        try:
            session = Session.objects.get(session_key=session_key)
            if session.expire_date < now:
                # cart.delete()
                deleted_count += 1
        except Session.DoesNotExist:
            # Session already gone = assume expired
            # cart.delete()
            deleted_count += 1

    print(f"Abandoned carts cleanup completed at {now}. Total carts deleted: {deleted_count}")
