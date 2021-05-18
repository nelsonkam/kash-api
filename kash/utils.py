from _blake2 import blake2b
from decimal import Decimal
from enum import Enum as BaseEnum
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money
from stellar_sdk import Server, Keypair, TransactionEnvelope, TransactionBuilder

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
    def get_xof_usd_deposit_rate():
        return convert_money(Money(1, "USD"), "XOF").amount + (
                Decimal(0.1) * convert_money(Money(1, "USD"), "XOF").amount)

    @staticmethod
    def get_xof_usd_withdrawal_rate():
        return convert_money(Money(1, "USD"), "XOF").amount - (
                Decimal(0.01) * convert_money(Money(1, "USD"), "XOF").amount)

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


class StellarHelpers:
    master_keypair = Keypair.from_secret(settings.STELLAR_MASTER_WALLET_SK)
    horizon_server = Server(horizon_url=settings.STELLAR_HORIZON_URL)

    @staticmethod
    def get_horizon_server():
        return Server(horizon_url=settings.STELLAR_HORIZON_URL)

    @staticmethod
    def get_master_account():
        return StellarHelpers.horizon_server.load_account(StellarHelpers.master_keypair.public_key)

    @staticmethod
    def get_account(account_id):
        return StellarHelpers.horizon_server.load_account(account_id)

    @staticmethod
    def submit_transaction(transaction: TransactionEnvelope):
        return StellarHelpers.horizon_server.submit_transaction(transaction)

    @staticmethod
    def submit_fee_bump_transaction(transaction: TransactionEnvelope):
        fee_bump = TransactionBuilder.build_fee_bump_transaction(
            fee_source=StellarHelpers.master_keypair,
            base_fee=1000,
            inner_transaction_envelope=transaction,
            network_passphrase=settings.STELLAR_NETWORK_PASSPHRASE
        )
        fee_bump.sign(StellarHelpers.master_keypair)
        return StellarHelpers.horizon_server.submit_transaction(fee_bump)

    @staticmethod
    def claim_pending_balances(keypair: Keypair):
        resp = StellarHelpers.horizon_server \
            .claimable_balances() \
            .for_claimant(keypair.public_key) \
            .order(True).call()
        records = resp.get("_embedded").get("records")
        if len(records) > 0:
            transaction = TransactionBuilder(
                source_account=StellarHelpers.get_account(keypair.public_key),
                network_passphrase=settings.STELLAR_NETWORK_PASSPHRASE,
                base_fee=1000
            )
            for balance in records:
                transaction = transaction.append_claim_claimable_balance_op(balance_id=balance.get('id'))
            transaction = transaction.build()
            transaction.sign(keypair)
            StellarHelpers.submit_fee_bump_transaction(transaction)
