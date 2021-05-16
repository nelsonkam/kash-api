from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.utils.timezone import now
from django_cryptography.fields import encrypt
from djmoney.contrib.exchange.models import convert_money
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from stellar_sdk import TransactionBuilder, Server, Keypair, Signer, Claimant, ClaimPredicate
from stellar_sdk.operation.create_claimable_balance import ClaimPredicateType

from core.models.base import BaseModel
from django.db import models
from django.db import IntegrityError

from kash.signals import transaction_status_changed
from kash.utils import TransactionStatusEnum, Conversions, TransactionType, StellarHelpers


class InsufficientBalance(IntegrityError):
    """Raised when a wallet has insufficient balance to
    run an operation.
    We're subclassing from :mod:`django.db.IntegrityError`
    so that it is automatically rolled-back during django's
    transaction lifecycle.
    """


class WalletManager(models.Manager):

    def create(self, **kwargs):
        keypair = Keypair.random()
        wallet = Wallet(
            **kwargs,
            external_id=keypair.public_key,
            secret_key=keypair.secret
        )
        master_keypair = Keypair.from_secret(settings.STELLAR_MASTER_WALLET_SK)
        transaction = TransactionBuilder(
            source_account=StellarHelpers.get_master_account(),
            network_passphrase=settings.STELLAR_NETWORK_PASSPHRASE,
            base_fee=100000
        ).append_begin_sponsoring_future_reserves_op(
            sponsored_id=keypair.public_key,
        ).append_create_account_op(
            destination=keypair.public_key,
            starting_balance="0",
        ).append_end_sponsoring_future_reserves_op(
            source=keypair.public_key
        ).append_begin_sponsoring_future_reserves_op(
            sponsored_id=keypair.public_key
        ).append_change_trust_op(
            asset_code=settings.USDC_ASSET.code,
            asset_issuer=settings.USDC_ASSET.issuer,
            source=keypair.public_key
        ).append_end_sponsoring_future_reserves_op(
            source=keypair.public_key
        ).append_begin_sponsoring_future_reserves_op(
            sponsored_id=keypair.public_key
        ).append_ed25519_public_key_signer(
            account_id=StellarHelpers.get_master_account().account_id,
            weight=1,
            source=keypair.public_key
        ).append_end_sponsoring_future_reserves_op(source=keypair.public_key).build()
        transaction.sign(keypair)
        transaction.sign(master_keypair)
        StellarHelpers.submit_transaction(transaction)
        wallet.save()
        return wallet

    def get_balance_wallet(self):
        return self.get(profile__kashtag="kash_balance")


class Wallet(BaseModel):
    profile = models.OneToOneField("kash.UserProfile", on_delete=models.CASCADE, related_name="wallet")
    external_id = models.CharField(max_length=255)
    secret_key = encrypt(models.CharField(max_length=255))

    objects = WalletManager()

    def get_account(self):
        return StellarHelpers.get_account(self.external_id)

    def get_transaction_builder(self):
        return TransactionBuilder(
            source_account=self.get_account(),
            network_passphrase=settings.STELLAR_NETWORK_PASSPHRASE,
            base_fee=1000
        )

    @property
    def xof_amount(self):
        return convert_money(Money(self.balance, "USD"), "XOF")

    @property
    def balance(self):
        server = StellarHelpers.get_horizon_server()
        balances = server.accounts().account_id(self.external_id).call().get("balances")
        balance = [balance for balance in balances if balance.get('asset_code') == settings.USDC_ASSET.code][0]
        return balance.get("balance")

    def transfer(self, wallet, amount: Money, narration: str = None):
        transaction = self.get_transaction_builder(
        ).append_payment_op(
            destination=wallet.external_id,
            amount=amount.amount,
            asset_code=settings.USDC_ASSET.code,
            asset_issuer=settings.USDC_ASSET.issuer
        )
        if narration:
            transaction = transaction.add_text_memo(narration)
        transaction = transaction.build()
        transaction.sign(StellarHelpers.master_keypair)
        StellarHelpers.submit_fee_bump_transaction(transaction)
        wallet.profile.push_notify(
            title="Le goût de ça 🤑",
            description=f"${wallet.profile.kashtag} vient de t'envoyer ${amount}",
        )

    def withdraw(self, amount: Money):
        from kash.models import Transaction
        transaction = self.get_transaction_builder(
        ).append_payment_op(
            destination=StellarHelpers.get_master_account().account_id,
            amount=amount.amount,
            asset_issuer=settings.USDC_ASSET.issuer,
            asset_code=settings.USDC_ASSET.code,
        ).add_text_memo("Retrait").build()
        transaction.sign(StellarHelpers.master_keypair)
        StellarHelpers.submit_fee_bump_transaction(transaction)

        xof_amount = amount.amount * Conversions.get_xof_usd_withdrawal_rate()
        payout_method = self.profile.momo_accounts.first()
        Transaction.objects.request(
            obj=self,
            name=self.profile.name,
            amount=xof_amount,
            phone=payout_method.phone,
            gateway=payout_method.gateway,
            initiator=self.profile.user,
            txn_type=TransactionType.payout
        )

    def initiate_deposit(self, amount: Money):
        claimants = [
            Claimant(self.external_id, ClaimPredicate.predicate_unconditional()),
            Claimant(StellarHelpers.master_keypair.public_key, ClaimPredicate.predicate_unconditional())
        ]
        transaction = TransactionBuilder(
            source_account=StellarHelpers.get_master_account(),
            network_passphrase=settings.STELLAR_NETWORK_PASSPHRASE,
            base_fee=1000
        ).append_create_claimable_balance_op(
            claimants=claimants,
            amount=amount.amount,
            asset=settings.USDC_ASSET,
        ).build()
        transaction.sign(StellarHelpers.master_keypair)
        StellarHelpers.submit_transaction(transaction)

    def deposit(self):
        resp = StellarHelpers.horizon_server.claimable_balances().for_claimant(self.external_id).order(True).call()
        records = resp.get("_embedded").get("records")
        transaction = self.get_transaction_builder()
        if len(records) > 0:
            for balance in records:
                transaction = transaction.append_claim_claimable_balance_op(balance_id=balance.get('id'))
            transaction = transaction.build()
            transaction.sign(StellarHelpers.master_keypair)
            StellarHelpers.submit_fee_bump_transaction(transaction)


@receiver(transaction_status_changed)
def deposit_wallet(sender, **kwargs):
    from kash.models import Notification
    txn = kwargs.pop("transaction")
    wallet_type = ContentType.objects.get_for_model(Wallet)
    if txn.content_type == wallet_type \
            and txn.transaction_type == TransactionType.payment \
            and txn.status == TransactionStatusEnum.failed.value:
        resp = StellarHelpers.horizon_server \
            .claimable_balances() \
            .for_claimant(StellarHelpers.master_keypair.public_key) \
            .order(True).call()
        records = resp.get("_embedded").get("records")
        if len(records) > 0:
            transaction = TransactionBuilder(
                source_account=StellarHelpers.get_master_account(),
                network_passphrase=settings.STELLAR_NETWORK_PASSPHRASE,
                base_fee=1000
            )
            for balance in records:
                transaction = transaction.append_claim_claimable_balance_op(balance_id=balance.get('id'))
            transaction = transaction.build()
            transaction.sign(StellarHelpers.master_keypair)
            StellarHelpers.submit_fee_bump_transaction(transaction)

    if txn.content_type == wallet_type \
            and txn.transaction_type == TransactionType.payment \
            and txn.status == TransactionStatusEnum.success.value:
        wallet = txn.content_object
        wallet.deposit()
