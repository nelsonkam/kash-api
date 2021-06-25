import re
from datetime import timedelta
from decimal import Decimal

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
from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money

from core.models.base import BaseModel
from core.utils.notify import tg_bot
from kash.utils import TransactionStatusEnum, Conversions


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

    def push_notify(self, title, description, obj=None):
        from kash.models import Notification
        notify = Notification.objects.create(
            title=title,
            description=description,
            content_object=obj,
            profile=self,
        )
        notify.send()

    @property
    def name(self):
        return self.user.name

    @property
    def phone_number(self):
        return self.user.phone_number

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
    def kyc_level(self):
        return 2 if self.kycdocument_set.filter(status="approved").exists() else 1

    @property
    def limits(self):
        xof_amount = self.wallet.xof_amount.amount
        withdrawal_fees = max(100, round(xof_amount * Decimal(0.02)))
        return {
            'sendkash': {
                'min': 25,
                'max': max(self.wallet.xof_amount.amount - 25, 0)
            },
            'deposit': {
                'min': 25,
                'max': 500000
            },
            'withdraw': {
                'min': 0,
                'max': xof_amount
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

    def __str__(self):
        return f'{self.name} (${self.kashtag})'

