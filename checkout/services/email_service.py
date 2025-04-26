from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_order_confirmation_email(order):
    subject = "Thank you for your order!"
    recipient_email = order.email if not order.user else order.user.email

    context = {
        'order': order,
    }
    html_message = render_to_string('emails/order_confirmation.html', context)

    send_mail(
        subject,
        '',  # Plain text version, can leave blank
        'no-reply@myshop.com',
        [recipient_email],
        html_message=html_message,
        fail_silently=False,
    )
