from django.db import models

from kash.providers.dummy import DummyProvider
from kash.providers.qosic import QosicProvider


class PaymentProvider(models.TextChoices):
    dummy = "dummy"
    qosic = "qosic"


def get_payment_provider(name):
    if name == PaymentProvider.qosic:
        return QosicProvider()
    elif name == PaymentProvider.dummy:
        return DummyProvider()
    else:
        raise NotImplementedError()
