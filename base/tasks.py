from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail
from todolist import settings
from base.models import EmailLog


@shared_task(bind=True)
def send_mail_func(self, subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
    )
    EmailLog.objects.create(user_email=recipient_list, subject=subject)
    return None
