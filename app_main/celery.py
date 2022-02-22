import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_main.settings")

app = Celery("app_main")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
