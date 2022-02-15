from django.db import models

from .dummy import DummyPaymentProvider
from .qosic import QosicProvider


class PaymentProvider(models.TextChoices):
    dummy = "dummy"
    qosic = "qosic"


def get_payment_provider(name):
    if name == PaymentProvider.qosic:
        return QosicProvider()
    elif name == PaymentProvider.dummy:
        return DummyPaymentProvider()
    else:
        raise NotImplementedError()
