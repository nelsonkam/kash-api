import re
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.postgres.fields import ArrayField
from django.core import validators
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import Sum, Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.deconstruct import deconstructible
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from core.models.base import BaseModel
from core.utils.notify import tg_bot
from kash.utils import TransactionStatusEnum


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
    avatar_url = models.URLField(blank=True)
    contacts = models.ManyToManyField('kash.UserProfile')

    @property
    def name(self):
        return self.user.name

    @property
    def txn_summary(self):
        from kash.models import KashTransaction
        received = Sum('amount', filter=Q(txn_type=KashTransaction.TxnType.credit,
                                          txn__status=TransactionStatusEnum.success.value,
                                          timestamp__gte=now() - timedelta(days=30)))
        sent = Sum('amount', filter=Q(txn_type=KashTransaction.TxnType.debit,
                                      txn__status=TransactionStatusEnum.success.value,
                                      timestamp__gte=now() - timedelta(days=30)))
        return {
            '30-days': self.kash_transactions.aggregate(received=received, sent=sent)
        }

    @property
    def limits(self):
        return {
            'sendkash': {
                'min': 25,
                'max': 100000
            },
            'purchase-card': {
                'min': 5,
                'max': 1000,
            },
            'fund-card': {
                'min': 5,
                'max': 1000
            }
        }


@receiver(post_save, sender=UserProfile)
def notify_tg(sender, instance, created, **kwargs):
    if created:
        tg_bot.send_message(chat_id=settings.TG_CHAT_ID, text=f"""
        New user of Kash!💪🏾

        Nom: {instance.name}
        Kashtag: ${instance.kashtag}

        {"_Ceci est un message test._" if settings.DEBUG else ""}
        """)
