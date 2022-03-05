from _blake2 import blake2b
from decimal import Decimal
from enum import Enum as BaseEnum
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from djmoney.money import Money


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
    moov = "moov-bj"
    mtn = "mtn-bj"


class Gateway(models.TextChoices):
    moov = "moov-bj"
    mtn = "mtn-bj"


GATEWAY_LIST = [Gateway.moov, Gateway.mtn]


class TransactionStatusEnum(Enum):
    pending = "pending"
    success = "success"
    failed = "failed"
    refunded = "refunded"


class TransactionStatus(models.TextChoices):
    pending = "pending"
    success = "success"
    failed = "failed"
    refunded = "refunded"


def generate_reference(digest_size=5):
    person = "".join(str(now().timestamp()).split("."))[:16]
    h = blake2b(digest_size=digest_size, person=person.encode())
    h.update(uuid4().hex.encode())
    return h.hexdigest()


def generate_reference_10():
    return generate_reference(digest_size=10)


class TransactionType(models.TextChoices):
    payment = "payment"
    payout = "payout"
    refund = "refund"


class Conversions:
    @staticmethod
    def get_usd_rate():
        return Decimal(615)

    @staticmethod
    def get_xof_from_usd(amount, is_withdrawal=False):
        from kash.payout.models import Rate

        rate = Rate.objects.get(code=Rate.Codes.rave_usd_ngn)
        ngn_rate = Money(rate.value, "NGN")
        rate_to_charge = (ngn_rate * settings.CONVERSION_RATES["NGN_XOF"]) / (1 - settings.CONVERSION_RATES["MARGIN"])
        rate_to_charge = rate_to_charge.amount - (
            rate_to_charge.amount * Decimal(settings.WITHDRAWAL_RATE) if is_withdrawal else 0
        )
        return Money(round(rate_to_charge * amount.amount), "XOF")

    @staticmethod
    def get_usd_from_xof(amount):
        rate = Conversions.get_xof_from_usd(Money(1, "USD"))

        return Money(amount.amount / rate.amount, "USD")


def compute_funding_earnings(txn_amount, funding_amount, funding_currency):
    from kash.payout.models import Rate

    if funding_currency == "NGN":
        ngn_rate = Rate.objects.get(code=Rate.Codes.rave_usd_ngn)
        xof_amount = Money(ngn_rate.value * funding_amount.amount, "XOF") * settings.CONVERSION_RATES["NGN_XOF"]
        return round(txn_amount - xof_amount)
    elif funding_currency == "USD":
        xof_amount = Conversions.get_xof_from_usd(funding_amount, is_withdrawal=True)
        return txn_amount - xof_amount
