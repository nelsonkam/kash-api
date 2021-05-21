import shlex
import subprocess

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery():
    cmd = 'pkill celery'
    subprocess.call(shlex.split(cmd))
    cmd = 'celery -A kash_api worker -l info --beat'
    subprocess.call(shlex.split(cmd))

class Command(BaseCommand):
    help = "Autoreload celery worker only for developement purposes."

    def handle(self, *args, **options):
        print('Starting celery worker with autoreload...')

        autoreload.run_with_reloader(restart_celery)
