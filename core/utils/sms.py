from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string


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
