from _blake2 import blake2b
from enum import Enum as BaseEnum
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from djmoney.contrib.exchange.models import convert_money
from moneyed import Money

from core.utils.payment import rave_request


class Enum(BaseEnum):
    @classmethod
    def keys(cls):
        return [k.name for k in cls]

    @classmethod
    def values(cls):
        return [k.value for k in cls]

    @classmethod
    def items(cls):
        return [(k.value, k.name) for k in cls]


class GatewayEnum(Enum):
    moov = 'moov-bj'
    mtn = 'mtn-bj'


class TransactionStatusEnum(Enum):
    pending = 'pending'
    success = 'success'
    failed = 'failed'
    refunded = 'refunded'


def generate_reference(digest_size=5):
    person = "".join(str(now().timestamp()).split('.'))[:16]
    h = blake2b(digest_size=digest_size, person=person.encode())
    h.update(uuid4().hex.encode())
    return h.hexdigest()


def generate_reference_10():
    return generate_reference(digest_size=10)


class TransactionType(models.TextChoices):
    payment = 'payment'
    payout = 'payout'
    refund = 'refund'


class Conversions:
    @staticmethod
    def get_xof_from_usd(amount, is_withdrawal=False):
        rates = rave_request("GET", f'/rates?from=USD&to=NGN&amount={float(amount.amount)}').json()
        amount_to_charge = Money(rates.get('data').get('to').get('amount'), "NGN")
        amount_to_charge = amount_to_charge * settings.CONVERSION_RATES['NGN_XOF']
        amount_to_charge = Money(amount_to_charge.amount, "XOF")
        margin = Money(amount.amount * 25, "XOF") if not is_withdrawal else Money(amount.amount * -25, "XOF")
        return amount_to_charge + margin

    @staticmethod
    def get_usd_from_xof(amount):
        rate = Conversions.get_xof_from_usd(Money(1, "USD"))

        return Money(amount.amount / rate.amount, "USD")
