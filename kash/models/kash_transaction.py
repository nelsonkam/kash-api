import random

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from core.models.base import BaseModel

from kash.signals import transaction_status_changed
from kash.utils import TransactionType, TransactionStatusEnum


class KashTransaction(BaseModel):
    class GroupMode(models.TextChoices):
        normal = 'normal'
        pacha = 'pacha'
        faro = 'faro'

    recipients = models.ManyToManyField('kash.UserProfile', related_name='kash_received')
    initiator = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE, related_name='kash_transactions')
    note = models.TextField()
    group_mode = models.CharField(max_length=10, blank=True, choices=GroupMode.choices)
    is_incognito = models.BooleanField(default=False)
    amount = MoneyField(max_digits=17, decimal_places=2, default_currency='XOF')
    paid_recipients = models.ManyToManyField('kash.UserProfile')

    @property
    def fees(self):
        amount = (
                self.amount * self.recipients.count()) if self.group_mode == KashTransaction.GroupMode.pacha else self.amount
        fee = amount * 0.03
        return fee if fee >= Money(100, "XOF") else Money(0, "XOF")

    @property
    def total(self):
        if self.group_mode == KashTransaction.GroupMode.pacha:
            return (self.amount * self.recipients.count()) + self.fees
        return self.amount + self.fees

    def pay(self, phone, gateway):
        from kash.models import Transaction

        return Transaction.objects.request(
            obj=self,
            name=self.initiator.name,
            amount=self.total.amount,
            initiator=self.initiator.user,
            phone=phone,
            gateway=gateway
        )

    def notify_recipient(self, recipient, amount):
        from kash.models import Notification
        amount = amount.amount if isinstance(amount, Money) else amount
        sender_name = "Quelqu'un" if self.is_incognito else f"${self.initiator.kashtag}"

        if self.group_mode == KashTransaction.GroupMode.faro:
            notif = Notification.objects.create(
                title="Le goût de ça 🤑",
                description=f"{sender_name} vient de te faroter {amount} FCFA pour \"{self.note}\"",
                content_object=self,
                profile=recipient
            )
            notif.send()
        else:
            notif = Notification.objects.create(
                title="Le goût de ça 🤑",
                description=f"{sender_name} vient de t'envoyer {amount} FCFA pour \"{self.note}\"",
                content_object=self,
                profile=recipient
            )
            notif.send()


@receiver(transaction_status_changed)
def payout_recipients(sender, **kwargs):
    from kash.models import Transaction

    txn = kwargs.pop("transaction")
    kash_txn_type = ContentType.objects.get_for_model(KashTransaction)

    def send_to_recipient(recipient, kash_txn, amount):
        if kash_txn.paid_recipients.filter(pk=recipient.id).exists():
            return
        payment_method = recipient.payout_methods.filter(gateway=txn.gateway).first()
        if not payment_method:
            payment_method = recipient.payout_methods.first()
        return Transaction.objects.request(
            obj=kash_txn,
            name=recipient.name,
            phone=payment_method.phone,
            gateway=payment_method.gateway,
            amount=amount,
            initiator=txn.initiator,
            txn_type=TransactionType.payout
        )

    if txn.content_type == kash_txn_type and txn.status == TransactionStatusEnum.success.value:
        kash_txn = txn.content_object
        if kash_txn.recipients.count() == 1:
            recipient = kash_txn.recipients.first()
            transaction = send_to_recipient(recipient, kash_txn, kash_txn.amount.amount)
            if transaction.status == TransactionStatusEnum.success.value:
                kash_txn.paid_recipients.add(recipient)
                kash_txn.save()
                kash_txn.notify_recipient(recipient, kash_txn.amount.amount)
        else:
            recipient_count = kash_txn.recipients.count()
            if kash_txn.group_mode == KashTransaction.GroupMode.normal:
                amount = round(kash_txn.amount / recipient_count) - Money(1, "XOF")
                for recipient in kash_txn.recipients.all():
                    transaction = send_to_recipient(recipient, kash_txn, amount.amount)
                    if transaction.status == TransactionStatusEnum.success.value:
                        kash_txn.notify_recipient(recipient, amount)
            elif kash_txn.group_mode == KashTransaction.GroupMode.pacha:
                for recipient in kash_txn.recipients.all():
                    transaction = send_to_recipient(recipient, kash_txn, kash_txn.amount.amount)
                    if transaction.status == TransactionStatusEnum.success.value:
                        kash_txn.notify_recipient(recipient, kash_txn.amount.amount)
            elif kash_txn.group_mode == KashTransaction.GroupMode.faro:
                r = [random.randint(1, 9) for i in range(0, recipient_count)]
                weights = [i/sum(r) for i in r]
                for index, recipient in enumerate(kash_txn.recipients.all()):
                    amount = round(kash_txn.amount * weights[index]) - Money(1, "XOF")
                    print(amount)
                    transaction = send_to_recipient(recipient, kash_txn, amount)
                    if transaction.status == TransactionStatusEnum.success.value:
                        kash_txn.notify_recipient(recipient, amount)
            else:
                raise NotImplemented()
