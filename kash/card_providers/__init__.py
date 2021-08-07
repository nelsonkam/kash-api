from django.db import models

from kash.card_providers.dummy import DummyCardProvider
from kash.card_providers.rave import RaveCardProvider


class CardProvider(models.TextChoices):
    rave = "rave"
    dummy = "dummy"


def get_card_provider(name):
    if name == CardProvider.rave:
        return RaveCardProvider()
    elif name == CardProvider.dummy:
        return DummyCardProvider()
    else:
        raise NotImplementedError()
