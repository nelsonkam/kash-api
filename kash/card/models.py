from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver
from django.utils.functional import cached_property
from djmoney.models.fields import MoneyField
from djmoney.money import Money, Currency
from rest_framework.exceptions import ValidationError

from kash.abstract.models import BaseModel
from kash.xlib.utils.notify import notify_telegram
from kash.xlib.signals import (
    transaction_status_changed,
    virtual_card_issued,
    virtual_card_funded,
)
from kash.xlib.utils.utils import (
    TransactionType,
    Conversions,
    TransactionStatus,
)

from .providers import CardProvider, get_card_provider


class VirtualCardManager(models.Manager):
    def create(self, *args, **kwargs):
        card = self.model(
            *args,
            **kwargs,
            provider_name=CardProvider.dummy
            if settings.DEBUG or settings.TESTING
            else CardProvider.rave,
        )
        card.save()
        return card


class VirtualCard(BaseModel):
    class Category(models.TextChoices):
        general = "general", "General"
        ads = "ads", "Ads"

    class Meta:
        db_table = "kash_virtualcard"

    external_id = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_permablocked = models.BooleanField(default=False)
    permablock_reason = models.CharField(max_length=255, blank=True)
    nickname = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True)
    profile = models.ForeignKey("kash_user.UserProfile", on_delete=models.CASCADE)
    last_4 = models.CharField(max_length=4, blank=True)
    provider_name = models.CharField(
        max_length=20, choices=CardProvider.choices, default=CardProvider.rave
    )

    objects = VirtualCardManager()

    _provider = None

    @property
    def issuance_cost(self):
        return Money(1000, "XOF")

    @property
    def card_type(self):
        return "visa"

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
        from kash.transaction.models import Transaction

        xof_amount = (
            amount
            if amount.currency == Currency("XOF")
            else Conversions.get_xof_from_usd(amount)
        )
        usd_amount = (
            amount
            if amount.currency == Currency("USD")
            else Conversions.get_usd_from_xof(amount)
        )

        if usd_amount < Money(5, usd_amount.currency):
            self.profile.push_notify(
                "Création de ta carte ⚠️",
                "Nous n'avons pas pu créer ta carte. Réessaies avec au moins $5.",
                self,
            )
            raise ValidationError("Minimum funding amount is $5.")

        txn = Transaction.objects.create(
            **{
                "obj": self,
                "name": self.profile.name,
                "amount": xof_amount + self.issuance_cost,
                "phone": phone,
                "gateway": gateway,
                "initiator": self.profile.user,
                "discount": Money(min(self.profile.promo_balance, 1000), "XOF"),
            }
        )
        FundingHistory.objects.create(
            txn_ref=txn.reference, card=self, amount=usd_amount, status="pending"
        )
        txn.request()
        return txn

    def create_external(self, usd_amount, txn, **kwargs):
        result = self.provider.issue(self, usd_amount)
        return result

    def fund_momo(self, amount, phone, gateway):
        from kash.transaction.models import Transaction

        xof_amount = Conversions.get_xof_from_usd(amount)

        if amount.amount < 5:
            self.profile.push_notify(
                "Recharge de ta carte ⚠️",
                "Nous n'avons pas pu recharger ta carte. Réessaies avec au moins $5.",
                self,
            )
            raise ValidationError("Minimum funding amount is $5.")

        total_amount = (
            xof_amount + self.issuance_cost if not self.external_id else xof_amount
        )

        txn = Transaction.objects.create(
            **{
                "obj": self,
                "name": self.profile.name,
                "amount": total_amount,
                "phone": phone,
                "gateway": gateway,
                "initiator": self.profile.user,
                "discount": Money(min(self.profile.promo_balance, 1000), "XOF"),
            }
        )
        FundingHistory.objects.create(
            txn_ref=txn.reference, card=self, amount=amount, status="pending"
        )
        txn.request()
        return txn

    def fund_external(self, amount, txn, **kwargs):
        if not self.external_id:
            return None
        result = self.provider.fund(self, amount)
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
        if not self.external_id:
            return None

        history = WithdrawalHistory.objects.create(
            card=self, amount=amount, status=WithdrawalHistory.Status.pending
        )
        self.provider.withdraw(self, amount)
        history.status = WithdrawalHistory.Status.withdrawn
        history.save(update_fields=["status"])
        history.payout(phone, gateway)

    def terminate(self):
        if not self.external_id:
            return None
        self.provider.terminate(self)
        self.external_id = ""
        self.is_active = False
        self.save()
        return


class FundingHistory(BaseModel):
    MAX_FUNDING_RETRIES = 2

    class FundingStatus(models.TextChoices):
        success = "success"
        failed = "failed"
        paid = "paid"
        pending = "pending"

    class Meta:
        db_table = "kash_fundinghistory"

    txn_ref = models.CharField(max_length=255, unique=True)
    card = models.ForeignKey(VirtualCard, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=17, decimal_places=2, default_currency="USD")
    status = models.CharField(max_length=15)
    retries = models.PositiveIntegerField(default=0)
    is_funding = models.BooleanField(default=False)

    def fund(self):
        from kash.transaction.models import Transaction

        if self.status != FundingHistory.FundingStatus.paid:
            return
        card = VirtualCard.objects.get(pk=self.card_id)

        # if deposit is being funded skip
        # else set deposit as being currently funded
        self.refresh_from_db()
        if self.is_funding:
            return
        else:
            self.is_funding = True
            self.save(update_fields=["is_funding"])

        # if we've already tried to fund this deposit and the balance is still
        # insufficient skip until balance is funded (i.e. sufficient)
        if self.retries > 0 and not card.provider.is_balance_sufficient(self.amount):
            self.is_funding = False
            self.save(update_fields=["is_funding"])
            return

        card = self.card
        txn = Transaction.objects.get(reference=self.txn_ref)
        result = {}
        operation = "funding" if card.external_id else "issuing"
        try:
            if not card.provider.is_balance_sufficient(self.amount):
                raise Exception("Insufficient balance on FLW")

            if card.external_id:
                result = card.fund_external(self.amount, txn)
            else:
                result = card.create_external(self.amount, txn)
            self.retries += 1
            self.status = FundingHistory.FundingStatus.success
            self.save()
        except Exception as err:
            self.retries += 1
            self.save()
            notify_telegram(
                chat_id=settings.TG_CHAT_ID,
                text=f"""
                       Card {'creation' if not card.external_id else 'funding'} failed!

                       Card: {card.external_id} (*{card.last_4})
                       Amount: {self.amount}
                       Reference: {self.txn_ref}
                       Retries: {self.retries}
                       Error: {err}

                       {"_Ceci est un message test._" if settings.DEBUG else ""}
                       """,
                disable_notification=True,
            )
            if self.retries == 1:
                card.profile.push_notify(
                    title="Création de votre carte️"
                    if not card.external_id
                    else "Recharge de votre carte️",
                    description=f"Veuillez patienter, la {'création' if not card.external_id else 'recharge'} "
                    f"de votre carte est en cours.",
                    obj=card,
                )
            if self.retries == self.MAX_FUNDING_RETRIES:
                self.status = FundingHistory.FundingStatus.failed
                self.save()

                Transaction.objects.get(reference=self.txn_ref).refund()

                description = (
                    "Nous n'avons pas pu créer votre carte et nous vous avons remboursé. "
                    "Veuillez réessayer avec au moins $5 ou dans 30 minutes."
                    if not card.external_id
                    else "Nous n'avons pas pu recharger votre carte et nous vous avons remboursé. "
                    "Veuillez réessayer dans 30 minutes."
                )
                card.profile.push_notify(
                    title="Création de votre carte ⚠️"
                    if not card.external_id
                    else "Recharge de votre carte ⚠️",
                    description=description,
                    obj=card,
                )
        finally:
            self.is_funding = False
            self.save(update_fields=["is_funding"])

        if self.status == FundingHistory.FundingStatus.success:
            if operation == "funding":
                virtual_card_funded.send(
                    sender=self.card.__class__,
                    card=self.card,
                    amount=self.amount,
                    txn=txn,
                    provider_data=result,
                )
            elif operation == "issuing":
                virtual_card_issued.send(
                    sender=self.card.__class__,
                    card=self.card,
                    amount=self.amount,
                    txn=txn,
                    provider_data=result,
                )


class WithdrawalHistory(BaseModel):
    class Status(models.TextChoices):
        paid_out = "paid-out"
        failed = "failed"
        pending = "pending"
        withdrawn = "withdrawn"

    class Meta:
        db_table = "kash_withdrawalhistory"

    txn_ref = models.CharField(max_length=255, blank=True)
    card = models.ForeignKey(VirtualCard, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=17, decimal_places=2, default_currency="XOF")
    status = models.CharField(max_length=15, choices=Status.choices)

    def payout(self, phone=None, gateway=None):
        from kash.transaction.models import Transaction

        if self.status != WithdrawalHistory.Status.withdrawn:
            return

        withdraw_amount = Conversions.get_xof_from_usd(self.amount, is_withdrawal=True)
        if not (phone and gateway):
            phone, gateway = self.card.profile.get_momo_account()

        if phone and gateway:
            txn = Transaction.objects.create(
                obj=self.card,
                name=self.card.profile.name,
                amount=withdraw_amount,
                phone=phone,
                gateway=gateway,
                initiator=self.card.profile.user,
                txn_type=TransactionType.payout,
            )
            self.txn_ref = txn.reference
            self.save()
            txn.payout()
            if txn.status == TransactionStatus.success:
                self.status = WithdrawalHistory.Status.paid_out
                self.save()


@receiver(transaction_status_changed)
def fund_card(sender, **kwargs):
    txn = kwargs.pop("transaction")
    vcard_type = ContentType.objects.get_for_model(VirtualCard)

    if txn.content_type == vcard_type and txn.status == TransactionStatus.failed:
        item = FundingHistory.objects.filter(
            txn_ref=txn.reference, card=txn.content_object
        ).first()
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
        f"Création de ta carte", f"Ta carte a été créée avec succès ✅.", card
    )


@receiver(virtual_card_funded)
def notify_card_funded(sender, **kwargs):
    card = kwargs.pop("card")
    card.profile.push_notify(
        f"Recharge de ta carte", f"Ta carte a été rechargée avec succès ✅.", card
    )


@receiver(virtual_card_issued)
def record_issuing_earning(sender, **kwargs):
    from kash.earning.models import Earning

    card = kwargs.pop("card")
    txn = kwargs.pop("txn")
    provider_data = kwargs.pop("provider_data")
    amount = kwargs.pop("amount")

    Earning.objects.record_issuing_earning(
        card=card,
        txn=txn,
        funding_amount=amount,
        funding_currency=provider_data.get("debit_currency", "NGN"),
    )


@receiver(virtual_card_funded)
def record_funding_earning(sender, **kwargs):
    from kash.earning.models import Earning

    card = kwargs.pop("card")
    txn = kwargs.pop("txn")
    provider_data = kwargs.pop("provider_data")
    amount = kwargs.pop("amount")

    Earning.objects.record_funding_earning(
        txn=txn,
        funding_amount=amount,
        funding_currency=provider_data.get("debit_currency", "NGN"),
    )
