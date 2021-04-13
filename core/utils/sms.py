from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string
from django.utils.timezone import now
from phone_verify.models import SMSVerification


def get_sms_backend():
    if settings.SMS_BACKEND:
        backend_import = settings.PHONE_VERIFICATION["BACKEND"]
    else:
        raise ImproperlyConfigured(
            "Please specify SMS_BACKEND within your settings"
        )
    backend_cls = import_string(backend_import)
    return backend_cls()


def send_sms(phone_number, message):
    backend = get_sms_backend()
    return backend.send_sms(phone_number, message)


def send_pending_messages():
    for message in SMSVerification.objects.filter(is_verified=False, created_at__gte=now() - timedelta(hours=3)):
        print(message.phone_number)
        send_sms(message.phone_number, f"L'envoi de code de verification est retablie. Toutes nos excuses a ceux qui n'ont pas recu leurs codes. #TeamKash")
