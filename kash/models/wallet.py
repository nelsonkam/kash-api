from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.utils.timezone import now
from djmoney.contrib.exchange.models import convert_money
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from core.models.base import BaseModel
from django.db import models
from django.db import IntegrityError

from kash.signals import transaction_status_changed
from kash.utils import TransactionStatusEnum, Conversions, TransactionType


class InsufficientBalance(IntegrityError):
    """Raised when a wallet has insufficient balance to
    run an operation.
    We're subclassing from :mod:`django.db.IntegrityError`
    so that it is automatically rolled-back during django's
    transaction lifecycle.
    """


class WalletManager(models.Manager):
    def get_balance_wallet(self):
        return self.get(profile__kashtag="kash_balance")


class Wallet(BaseModel):
    profile = models.ForeignKey("kash.UserProfile", on_delete=models.CASCADE, related_name="wallets")
    balance = MoneyField(max_digits=17, decimal_places=2, default_currency="USD", default=Money(0, "USD"))

    objects = WalletManager()

    @property
    def xof_amount(self):
        return convert_money(self.balance, "XOF")

    def credit(self, amount, **kwargs):
        self.transactions.create(
            amount=amount,
            running_balance=self.balance + amount,
            timestamp=now(),
            **kwargs
        )
        self.balance += amount
        self.save()

    def debit(self, amount, **kwargs):
        if amount > self.balance:
            raise InsufficientBalance('This wallet has insufficient balance.')

        self.transactions.create(
            amount=-amount,
            running_balance=self.balance - amount,
            timestamp=now(),
            **kwargs
        )
        self.balance -= amount
        self.save()

    def transfer(self, wallet, amount, debit_merchant, credit_merchant, narration=None):
        self.debit(amount, merchant=debit_merchant, narration=narration)
        wallet.credit(amount, merchant=credit_merchant, narration=narration)

    def withdraw(self, amount):
        from kash.models import Transaction
        xof_amount = amount.amount * Conversions.get_xof_usd_withdrawal_rate()
        payout_method = self.profile.momo_accounts.first()
        txn = Transaction.objects.request(
            obj=self,
            name=self.profile.name,
            amount=xof_amount,
            phone=payout_method.phone,
            gateway=payout_method.gateway,
            initiator=self.profile.user,
            txn_type=TransactionType.payout
        )
        balance_wallet = Wallet.objects.get_balance_wallet()
        self.transfer(balance_wallet, amount, debit_merchant="Retrait",
                      credit_merchant=f"Retrait de ${self.profile.kashtag}", narration=f"Ref: {txn.reference}")

    def deposit(self, amount, reference):
        balance_wallet = Wallet.objects.get_balance_wallet()
        amount = amount.amount / Conversions.get_xof_usd_deposit_rate()
        balance_wallet.transfer(self, Money(amount, "USD"),
                                debit_merchant=f"Recharge pour ${self.profile.kashtag}",
                                credit_merchant=f"Recharge", narration=f"Ref: {reference}")


class WalletTransaction(BaseModel):
    amount = MoneyField(max_digits=17, decimal_places=2, default_currency="USD")
    running_balance = MoneyField(max_digits=17, decimal_places=2, default_currency="USD")
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    merchant = models.CharField(max_length=255)
    timestamp = models.DateTimeField(null=True)
    narration = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=False)


@receiver(transaction_status_changed)
def deposit_wallet(sender, **kwargs):
    from kash.models import Notification
    txn = kwargs.pop("transaction")
    wallet_type = ContentType.objects.get_for_model(Wallet)

    if txn.content_type == wallet_type and txn.status == TransactionStatusEnum.success.value:
        wallet = txn.content_object
        if not wallet.transactions.filter(narration=f"Ref: {txn.reference}").exists():
            wallet.deposit(txn.amount, txn.reference)
