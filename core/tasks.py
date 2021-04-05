from celery import shared_task
from django.conf import settings
from django.utils.module_loading import import_string


@shared_task
def update_rates():
    backend = import_string(settings.EXCHANGE_BACKEND)()
    backend.update_rates()
