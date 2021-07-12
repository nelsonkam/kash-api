from decimal import Decimal

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
        ).build()
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
    is_active = models.BooleanField(default=True)

    objects = WalletManager()

    def get_account(self):
        return StellarHelpers.get_account(self.external_id)

    def get_transaction_builder(self):
        return TransactionBuilder(
            source_account=self.get_account(),
            network_passphrase=settings.STELLAR_NETWORK_PASSPHRASE,
            base_fee=100000
        )

    @property
    def keypair(self):
        return Keypair.from_secret(str(self.secret_key))

    @property
    def xof_amount(self):
        if not self.is_active:
            return Money(0, "XOF")
        return Money(Decimal(self.balance) * Conversions.get_usd_rate(), "XOF")

    @property
    def balance(self):
        if not self.is_active:
            return 0
        server = StellarHelpers.get_horizon_server()
        balances = server.accounts().account_id(self.external_id).call().get("balances")
        balance = [balance for balance in balances if balance.get('asset_code') == settings.USDC_ASSET.code][0]
        return balance.get("balance")

    def bulk_transfer(self, wallets, amount: Money, narration: str = None):
        if len(wallets) == 0:
            return

        transaction = self.get_transaction_builder()
        xof_amount = amount * Conversions.get_usd_rate()

        for wallet in wallets:
            transaction.append_payment_op(
                destination=wallet.external_id,
                amount=round(amount.amount, 7),
                asset_code=settings.USDC_ASSET.code,
                asset_issuer=settings.USDC_ASSET.issuer
            )
        if round(xof_amount.amount * len(wallets)) >= 1000:
            transaction.append_payment_op(
                destination=StellarHelpers.get_master_account().account_id,
                amount=round(Decimal(25) / Conversions.get_usd_rate(), 7),
                asset_code=settings.USDC_ASSET.code,
                asset_issuer=settings.USDC_ASSET.issuer
            )
        if narration:
            transaction = transaction.add_text_memo(narration[0:28])
        transaction = transaction.build()
        transaction.sign(self.keypair)
        StellarHelpers.submit_fee_bump_transaction(transaction)

        for wallet in wallets:
            wallet.profile.push_notify(
                obj=wallet,
                title="Le goût de ça 🤑",
                description=f"${self.profile.kashtag} vient de t'envoyer CFA {round(xof_amount.amount)}",
            )

    def transfer(self, wallet, amount: Money, narration: str = None):
        return self.bulk_transfer([wallet], amount, narration)

    def pay(self, amount: Money, memo: str):
        transaction = self.get_transaction_builder(
        ).append_payment_op(
            destination=StellarHelpers.get_master_account().account_id,
            amount=amount.amount,
            asset_issuer=settings.USDC_ASSET.issuer,
            asset_code=settings.USDC_ASSET.code,
        ).add_text_memo(memo[0:28]).build()
        transaction.sign(self.keypair)
        StellarHelpers.submit_fee_bump_transaction(transaction)

    def withdraw(self, amount: Money, phone: str, gateway: str):
        from kash.models import Transaction
        transaction = self.get_transaction_builder(
        ).append_payment_op(
            destination=StellarHelpers.get_master_account().account_id,
            amount=amount.amount,
            asset_issuer=settings.USDC_ASSET.issuer,
            asset_code=settings.USDC_ASSET.code,
        ).add_text_memo("Retrait").build()
        transaction.sign(self.keypair)
        StellarHelpers.submit_fee_bump_transaction(transaction)

        xof_amount = (amount.amount * Conversions.get_usd_rate())
        xof_amount -= max(100, round(xof_amount * Decimal(0.02)))
        if xof_amount > 0:
            Transaction.objects.request(
                obj=self,
                name=self.profile.name,
                amount=xof_amount,
                phone=phone,
                gateway=gateway,
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
            base_fee=100000
        ).append_create_claimable_balance_op(
            claimants=claimants,
            amount=amount.amount,
            asset=settings.USDC_ASSET,
        ).build()
        transaction.sign(StellarHelpers.master_keypair)
        StellarHelpers.submit_transaction(transaction)

    def deposit(self, amount):
        transaction = TransactionBuilder(
            source_account=StellarHelpers.get_master_account(),
            network_passphrase=settings.STELLAR_NETWORK_PASSPHRASE,
            base_fee=100000
        ).append_payment_op(
            destination=self.profile.wallet.external_id,
            amount=round(amount.amount / Conversions.get_usd_rate(), 7),
            asset_issuer=settings.USDC_ASSET.issuer,
            asset_code=settings.USDC_ASSET.code
        ).add_text_memo(f'Recharge').build()
        transaction.sign(StellarHelpers.master_keypair)
        StellarHelpers.submit_transaction(transaction)

    def deactivate(self):
        if round(self.xof_amount.amount) == 0:

            transaction = self.get_transaction_builder()
            if 0 < float(self.balance) < 1:
                transaction = transaction.append_payment_op(
                    destination=StellarHelpers.get_master_account().account_id,
                    amount=self.balance,
                    asset_issuer=settings.USDC_ASSET.issuer,
                    asset_code=settings.USDC_ASSET.code,
                ).add_text_memo("Deactivation")
            transaction = transaction.append_change_trust_op(
                asset_code=settings.USDC_ASSET.code,
                asset_issuer=settings.USDC_ASSET.issuer,
                limit=Decimal(0)
            ).append_account_merge_op(
                destination=StellarHelpers.master_keypair.public_key
            ).build()
            transaction.sign(self.keypair)
            StellarHelpers.submit_fee_bump_transaction(transaction)
            self.is_active = False
            self.save()


class WalletFundingHistory(BaseModel):
    class FundingStatus(models.TextChoices):
        success = 'success'
        failed = 'failed'
        pending = 'pending'

    txn_ref = models.CharField(max_length=255, unique=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    status = models.CharField(max_length=15)


class WalletTransaction(BaseModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    is_successful = models.BooleanField()
    cursor = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    amount = MoneyField(max_digits=17, decimal_places=0, default_currency="XOF")
    txn_type = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    memo = models.CharField(max_length=32, blank=True)
    external_id = models.CharField(max_length=255)


@receiver(transaction_status_changed)
def deposit_wallet(sender, **kwargs):
    from kash.models import Notification
    txn = kwargs.pop("transaction")
    wallet_type = ContentType.objects.get_for_model(Wallet)

    if txn.content_type == wallet_type \
            and txn.transaction_type == TransactionType.payment \
            and txn.status == TransactionStatusEnum.success.value:
        wallet = txn.content_object
        item = WalletFundingHistory.objects.filter(
            txn_ref=txn.reference,
            wallet=wallet,
            status=WalletFundingHistory.FundingStatus.pending
        ).first()
        if item:
            wallet.deposit(txn.amount)
            item.status = WalletFundingHistory.FundingStatus.success
            item.save()
