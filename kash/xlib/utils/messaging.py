from datetime import timedelta
from time import sleep

import messagebird
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.module_loading import import_string
from django.utils.timezone import now
from phone_verify.models import SMSVerification


def get_sms_backend(backend):
    if not backend:
        raise ImproperlyConfigured("Please specify SMS_BACKEND within your settings")
    backend_cls = import_string(backend)
    return backend_cls()


def send_sms(phone_number, message, backend=settings.SMS_BACKEND):
    backend = get_sms_backend(backend)
    return backend.send_sms(phone_number, message)


def send_email(email_address, subject, template, context):
    html_body = render_to_string(template, context)
    message = EmailMultiAlternatives(
        subject=subject, from_email="Kash <support@kweek.africa>", to=[email_address]
    )
    message.attach_alternative(html_body, "text/html")
    message.send(fail_silently=False)
