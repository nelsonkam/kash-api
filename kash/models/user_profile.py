import re

from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.postgres.fields import ArrayField
from django.core import validators
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from core.models.base import BaseModel
from core.utils.notify import tg_bot


@deconstructible
class KashtagValidator(validators.RegexValidator):
    regex = r'^[\w]+\Z'
    message = _(
        'Enter a valid kashtag. This value may contain only English letters, '
        'numbers, and _ characters.'
    )
    flags = re.ASCII


class UserProfile(BaseModel):
    user = models.OneToOneField('core.User', on_delete=models.CASCADE, related_name='profile')
    kashtag = models.CharField(max_length=30, unique=True, validators=[KashtagValidator, MinLengthValidator(3)])
    device_ids = ArrayField(models.CharField(max_length=255), default=list)

    @property
    def name(self):
        return self.user.name


@receiver(post_save, sender=UserProfile)
def notify_tg(sender, instance, created, **kwargs):
    if created:
        tg_bot.send_message(chat_id=settings.TG_CHAT_ID, text=f"""
        New user of Kash!💪🏾

        Nom: {instance.name}
        Kashtag: ${instance.kashtag}

        {"_Ceci est un message test._" if settings.DEBUG else ""}
        """)
