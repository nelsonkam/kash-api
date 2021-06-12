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
    def get_usd_rate():
        return Decimal(615)

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
            base_fee=100000,
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
                base_fee=100000
            )
            for balance in records:
                transaction = transaction.append_claim_claimable_balance_op(balance_id=balance.get('id'))
            transaction = transaction.build()
            transaction.sign(keypair)
            StellarHelpers.submit_fee_bump_transaction(transaction)

    @staticmethod
    def format_payment_transactions(wallet, payments):
        from kash.models import Wallet

        source_accts = Wallet.objects.filter(
            external_id__in=[payment.get('to') for payment in payments] + [payment.get('from') for payment in payments]
        ).distinct('external_id').values_list('profile__kashtag', 'external_id')
        source_accts = list(source_accts)

        def get_kashtag(txn):
            source_account = txn.get('to') if txn.get('from') == wallet.external_id else txn.get('from')
            if source_account == StellarHelpers.master_keypair.public_key:
                return "Kash"
            else:
                kashtags = [kashtag for kashtag, external_id in source_accts if external_id == source_account]
                return f"${kashtags[0]}" if len(kashtags) > 0 else "Anonyme"

        def get_memo(txn):
            data = StellarHelpers.horizon_server.transactions().transaction(txn.get('transaction_hash')).call()
            if data.get('memo_type') == 'text':
                return data.get('memo')
            return None

        return [{
            'id': payment.get('id'),
            'cursor': payment.get('paging_token'),
            'successful': payment.get('transaction_successful'),
            'created_at': payment.get('created_at'),
            'type': 'debit' if payment.get('from') == wallet.external_id else 'credit',
            'amount': Decimal(payment.get('amount')) * Conversions.get_usd_rate(),
            'source': get_kashtag(payment),
            'memo': get_memo(payment),
            'account_id': payment.get('to') if payment.get('from') == wallet.external_id else payment.get('from')
        } for payment in payments if payment.get("type") == "payment"]

    @staticmethod
    def format_payment_transaction(wallet, payment):
        return StellarHelpers.format_payment_transactions(wallet, [payment])


def get_balances():
    from kash.models import Wallet
    balance = Decimal(0)
    total = 0
    card_holder_total = 0
    for wallet in Wallet.objects.all():
        if float(wallet.balance) > 0:
            balance += Decimal(wallet.balance)
            card_count = wallet.profile.virtualcard_set.count()
            card_holder_total += 0 if card_count == 0 else 1
            print(
                f"{wallet.profile}: ${wallet.balance} ({wallet.xof_amount}) | Cards: {card_count}"
            )
        total += 1
    print(f"\n\nTotal: ${balance} ({balance * Conversions.get_usd_rate()} XOF)")
    print(f"Total !0 users: {total} | Cardholder !0 users: {card_holder_total}")
