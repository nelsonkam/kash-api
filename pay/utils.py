from _blake2 import blake2b
from enum import Enum as BaseEnum
from uuid import uuid4

from django.utils.timezone import now


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
    moov = 'MOOV MONEY'
    mtn = 'MTN MOBILE MONEY'


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
