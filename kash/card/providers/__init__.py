from kash.xlib.enums import CardProvider

from .dummy import DummyCardProvider
from .rave import RaveCardProvider


def get_card_provider(name):
    if name == CardProvider.rave:
        return RaveCardProvider()
    elif name == CardProvider.dummy:
        return DummyCardProvider()
    else:
        raise NotImplementedError()
