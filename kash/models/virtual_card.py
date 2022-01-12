import re
import secrets
from datetime import timedelta, date
from urllib import parse

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver
from django.utils.functional import cached_property
from djmoney.models.fields import MoneyField
from djmoney.money import Money, Currency
from rest_framework.exceptions import ValidationError

from core.models.base import BaseModel
from core.utils.notify import tg_bot, notify_telegram
from core.utils.payment import rave_request, rave2_request
from kash.card_providers import CardProvider, get_card_provider
from kash.signals import transaction_status_changed, virtual_card_issued, virtual_card_funded
from kash.utils import TransactionStatusEnum, TransactionType, Conversions, TransactionStatus


class VirtualCardManager(models.Manager):

    def create(self, *args, **kwargs):
        card = self.model(
            *args,
            **kwargs,
            provider_name=CardProvider.dummy if settings.DEBUG or settings.TESTING else CardProvider.rave
        )
        card.save()
        return card


class VirtualCard(BaseModel):
    class Category(models.TextChoices):
        general = "general", "General"
        ads = "ads", "Ads"

    external_id = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    nickname = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True)
    profile = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE)
    last_4 = models.CharField(max_length=4, blank=True)
    provider_name = models.CharField(max_length=20, choices=CardProvider.choices, default=CardProvider.rave)

    objects = VirtualCardManager()

    _provider = None

    @property
    def issuance_cost(self):
        return Money(1000, 'XOF')

    @property
    def card_type(self):
        return 'visa'

    @cached_property
    def provider(self):
        if self._provider:
            return self._provider
        self._provider = get_card_provider(self.provider_name)
        return self._provider

    @property
    def card_details(self):
        return self.provider.get_details(self)

    def get_statement(self):
        return self.provider.get_statement(self)

    def get_transactions(self):
        if not self.external_id:
            return None
        return self.provider.get_transactions(self)

    def purchase_momo(self, amount, phone, gateway):
        from kash.models import Transaction
        xof_amount = amount if amount.currency == Currency('XOF') else Conversions.get_xof_from_usd(amount)
        usd_amount = amount if amount.currency == Currency('USD') else Conversions.get_usd_from_xof(amount)

        if usd_amount < Money(5, usd_amount.currency):
            self.profile.push_notify(
                "Création de ta carte ⚠️",
                "Nous n'avons pas pu créer ta carte. Réessaies avec au moins $5.",
                self
            )
            raise ValidationError("Minimum funding amount is $5.")

        txn = Transaction.objects.create(**{
            'obj': self,
            'name': self.profile.name,
            'amount': xof_amount + self.issuance_cost,
            'phone': phone,
            'gateway': gateway,
            'initiator': self.profile.user,
            'discount': Money(min(self.profile.promo_balance, 1000), "XOF")
        })
        FundingHistory.objects.create(txn_ref=txn.reference, card=self, amount=usd_amount, status='pending')
        txn.request()
        return txn

    def create_external(self, usd_amount, txn, **kwargs):
        result = self.provider.issue(self, usd_amount)
        virtual_card_issued.send(sender=self.__class__, card=self, amount=usd_amount, txn=txn, provider_data=result)

    def fund_momo(self, amount, phone, gateway):
        from kash.models import Transaction
        xof_amount = Conversions.get_xof_from_usd(amount)

        if amount.amount < 5:
            self.profile.push_notify(
                "Recharge de ta carte ⚠️",
                "Nous n'avons pas pu recharger ta carte. Réessaies avec au moins $5.",
                self
            )
            raise ValidationError("Minimum funding amount is $5.")

        total_amount = xof_amount + self.issuance_cost if not self.external_id else xof_amount

        txn = Transaction.objects.create(**{
            'obj': self,
            'name': self.profile.name,
            'amount': total_amount,
            'phone': phone,
            'gateway': gateway,
            'initiator': self.profile.user,
            'discount': Money(min(self.profile.promo_balance, 1000), "XOF")
        })
        FundingHistory.objects.create(txn_ref=txn.reference, card=self, amount=amount, status='pending')
        txn.request()
        return txn

    def fund_external(self, amount, txn, **kwargs):
        if not self.external_id:
            return None
        result = self.provider.fund(self, amount)
        virtual_card_funded.send(sender=self.__class__, card=self, amount=amount, txn=txn, provider_data=result)
        return result


    def freeze(self):
        if not self.external_id:
            return None
        self.provider.freeze(self)
        self.is_active = False
        self.save()
        return

    def unfreeze(self):
        if not self.external_id:
            return None
        self.provider.unfreeze(self)
        self.is_active = True
        self.save()
        return

    def withdraw(self, amount, phone=None, gateway=None):
        from kash.models import Transaction

        if not self.external_id:
            return None

        history = WithdrawalHistory.objects.create(card=self, amount=amount, status=WithdrawalHistory.Status.pending)
        self.provider.withdraw(self, amount)
        history.status = WithdrawalHistory.Status.withdrawn
        history.save(update_fields=['status'])

        withdraw_amount = Conversions.get_xof_from_usd(amount, is_withdrawal=True)
        if not (phone and gateway):
            phone, gateway = self.profile.get_momo_account()

        if phone and gateway:
            txn = Transaction.objects.create(
                obj=self,
                name=self.profile.name,
                amount=withdraw_amount,
                phone=phone,
                gateway=gateway,
                initiator=self.profile.user,
                txn_type=TransactionType.payout
            )
            history.txn_ref = txn.reference
            history.save()
            txn.payout()
            if txn.status == TransactionStatus.success:
                history.status = WithdrawalHistory.Status.paid_out
                history.save()

    def terminate(self):
        if not self.external_id:
            return None
        self.provider.terminate(self)
        self.external_id = ''
        self.is_active = False
        self.save()
        return


class FundingHistory(BaseModel):
    MAX_FUNDING_RETRIES = 4
    class FundingStatus(models.TextChoices):
        success = 'success'
        failed = 'failed'
        paid = 'paid'
        pending = 'pending'

    txn_ref = models.CharField(max_length=255, unique=True)
    card = models.ForeignKey(VirtualCard, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=17, decimal_places=2, default_currency="USD")
    status = models.CharField(max_length=15)
    retries = models.PositiveIntegerField(default=0)

    def fund(self):
        from kash.models import Transaction
        if self.status != FundingHistory.FundingStatus.paid:
            return

        if self.retries > 0 and not self.card.provider.is_balance_sufficient(self.amount):
            return

        card = self.card
        txn = Transaction.objects.get(reference=self.txn_ref)
        try:
            if card.external_id:
                card.fund_external(self.amount, txn)
            else:
                card.create_external(self.amount, txn)
            self.retries += 1
            self.status = FundingHistory.FundingStatus.success
            self.save()
        except Exception as err:
            raise err
            self.retries += 1
            self.save()
            notify_telegram(chat_id=settings.TG_CHAT_ID, text=f"""
                       Card {'creation' if not card.external_id else 'funding'} failed!

                       Card: {card.external_id} (*{card.last_4})
                       Amount: {self.amount}
                       Reference: {self.txn_ref}
                       Retries: {self.retries}
                       Error: {err}

                       {"_Ceci est un message test._" if settings.DEBUG else ""}
                       """, disable_notification=True)
            if self.retries == 1:
                card.profile.push_notify(
                    title="Création de votre carte️" if not card.external_id else "Recharge de votre carte️",
                    description=f"Veuillez patienter, la {'création' if not card.external_id else 'recharge'} "
                                f"de votre carte est en cours.",
                    obj=card
                )
            if self.retries == self.MAX_FUNDING_RETRIES:
                self.status = FundingHistory.FundingStatus.failed
                self.save()

                Transaction.objects.get(reference=self.txn_ref).refund()

                description = "Nous n'avons pas pu créer votre carte et nous vous avons remboursé. " \
                              "Veuillez réessayer avec au moins $5 ou dans 30 minutes." \
                    if not card.external_id \
                    else "Nous n'avons pas pu recharger votre carte et nous vous avons rembourséd. " \
                         "Veuillez réessayer dans 30 minutes."
                card.profile.push_notify(
                    title="Création de votre carte ⚠️" if not card.external_id else "Recharge de votre carte ⚠️",
                    description=description,
                    obj=card
                )


class WithdrawalHistory(BaseModel):
    class Status(models.TextChoices):
        paid_out = 'paid-out'
        failed = 'failed'
        pending = 'pending'
        withdrawn = 'withdrawn'

    txn_ref = models.CharField(max_length=255, blank=True)
    card = models.ForeignKey(VirtualCard, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=17, decimal_places=2, default_currency="XOF")
    status = models.CharField(max_length=15, choices=Status.choices)


class CardTransaction(BaseModel):
    card = models.ForeignKey(VirtualCard, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=17, decimal_places=2, default_currency="USD")
    product = models.TextField(null=True)
    reference_details = models.TextField(null=True)
    narration = models.TextField(null=True)
    external_id = models.CharField(max_length=255, unique=True)
    txn_type = models.CharField(max_length=10, null=True)
    status = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(null=True)


@receiver(transaction_status_changed)
def fund_card(sender, **kwargs):
    txn = kwargs.pop("transaction")
    vcard_type = ContentType.objects.get_for_model(VirtualCard)

    if txn.content_type == vcard_type and txn.status == TransactionStatus.failed:
        item = FundingHistory.objects.filter(txn_ref=txn.reference, card=txn.content_object).first()
        if item:
            item.status = FundingHistory.FundingStatus.failed
            item.save()

    if txn.content_type == vcard_type and txn.status == TransactionStatus.success:
        card = txn.content_object
        item = FundingHistory.objects.filter(txn_ref=txn.reference, card=card).first()
        if item and item.status != FundingHistory.FundingStatus.success:
            item.status = FundingHistory.FundingStatus.paid
            item.save()
            item.fund()


@receiver(virtual_card_issued)
def notify_card_issued(sender, **kwargs):
    card = kwargs.pop("card")
    card.profile.push_notify(
        f"Création de ta carte",
        f"Ta carte a été créée avec succès ✅.",
        card
    )

@receiver(virtual_card_funded)
def notify_card_funded(sender, **kwargs):
    card = kwargs.pop("card")
    card.profile.push_notify(
        f"Recharge de ta carte",
        f"Ta carte a été rechargée avec succès ✅.",
        card
    )



@receiver(virtual_card_issued)
def record_issuing_earning(sender, **kwargs):
    from kash.models import Earning
    card = kwargs.pop("card")
    txn = kwargs.pop("txn")
    provider_data = kwargs.pop("provider_data")
    amount = kwargs.pop('amount')

    Earning.objects.record_issuing_earning(
        card=card,
        txn=txn,
        funding_amount=amount,
        funding_currency=provider_data.get("debit_currency", "NGN")
    )

@receiver(virtual_card_funded)
def record_funding_earning(sender, **kwargs):
    from kash.models import Earning
    txn = kwargs.pop("txn")
    provider_data = kwargs.pop("provider_data")
    amount = kwargs.pop('amount')

    Earning.objects.record_funding_earning(
        txn=txn,
        funding_amount=amount,
        funding_currency=provider_data.get("debit_currency", "NGN")
    )