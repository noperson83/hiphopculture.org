from django.core.mail import send_mail
from .models import Subscriber

def send_mailing_list_email(subject, message):
    subscribers = Subscriber.objects.all()
    recipient_list = [subscriber.email for subscriber in subscribers]
    send_mail(
        subject,
        message,
        'labmunkzink@gmail.com',  # Replace with your email
        recipient_list,
        fail_silently=False,
    )
