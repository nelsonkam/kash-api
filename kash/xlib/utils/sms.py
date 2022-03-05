from datetime import timedelta
from time import sleep

import messagebird
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
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


def send_pending_messages():
    for message in SMSVerification.objects.filter(is_verified=False, created_at__gte=now() - timedelta(hours=3)):

        client = messagebird.Client(settings.MESSAGEBIRD_ACCESS_KEY)
        client.message_create(
            "Kash",
            str(message.phone_number),
            f"L'envoi de code de verification est retablie. Toutes nos excuses a ceux qui n'ont pas recu leurs codes. #TeamKash",
            {"reference": "none"},
        )
        sleep(1)
