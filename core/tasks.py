from django.conf import settings
from django.utils.module_loading import import_string
from huey import crontab
from huey.contrib.djhuey import db_periodic_task


@db_periodic_task(crontab(hour='1', minute='0'))
def update_rates():
    backend = import_string(settings.EXCHANGE_BACKEND)()
    backend.update_rates()
