import random

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver
from django.utils.timezone import now
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from core.models.base import BaseModel

from kash.signals import transaction_status_changed
from kash.utils import TransactionType, TransactionStatusEnum


class SendKash(BaseModel):
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
                self.amount * self.recipients.count()) if self.group_mode == SendKash.GroupMode.pacha else self.amount
        fee = amount * 0.03
        return fee if fee >= Money(100, "XOF") else Money(0, "XOF")

    @property
    def total(self):
        if self.group_mode == SendKash.GroupMode.pacha:
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

        if self.group_mode == SendKash.GroupMode.faro:
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

    def record_transaction(self, recipient, amount, payment_txn, payout_txn):
        from kash.models import KashTransaction
        KashTransaction.objects.create(
            amount=amount,
            sender=self.initiator,
            receiver=recipient,
            profile=self.initiator,
            txn_ref=payment_txn.reference,
            narration=self.note,
            txn_type=KashTransaction.TxnType.debit,
            timestamp=now()
        )
        KashTransaction.objects.create(
            amount=payout_txn.amount,
            sender=self.initiator,
            receiver=recipient,
            profile=recipient,
            txn_ref=payout_txn.reference,
            narration=self.note,
            txn_type=KashTransaction.TxnType.credit,
            timestamp=now()
        )


@receiver(transaction_status_changed)
def payout_recipients(sender, **kwargs):
    from kash.models import Transaction, KashTransaction

    txn = kwargs.pop("transaction")
    kash_txn_type = ContentType.objects.get_for_model(SendKash)

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
        send_kash = txn.content_object
        fee_txn = KashTransaction(
            amount=send_kash.fees,
            sender=send_kash.initiator,
            receiver=send_kash,
            profile=send_kash.initiator,
            txn_ref=txn.reference,
            narration="Frais de transaction",
            txn_type=KashTransaction.TxnType.debit,
            timestamp=now()
        )
        if send_kash.recipients.count() == 1:
            recipient = send_kash.recipients.first()
            transaction = send_to_recipient(recipient, send_kash, send_kash.amount.amount)
            if transaction.status == TransactionStatusEnum.success.value:
                send_kash.record_transaction(recipient, send_kash.amount, txn, transaction)
                send_kash.paid_recipients.add(recipient)
                send_kash.save()
                send_kash.notify_recipient(recipient, send_kash.amount.amount)
        else:
            recipient_count = send_kash.recipients.count()
            if send_kash.group_mode == SendKash.GroupMode.normal:
                amount = round(send_kash.amount / recipient_count) - Money(1, "XOF")
                total_amount = Money(0, "XOF")
                for recipient in send_kash.recipients.all():
                    transaction = send_to_recipient(recipient, send_kash, amount.amount)
                    if transaction.status == TransactionStatusEnum.success.value:
                        send_kash.record_transaction(recipient, amount, txn, transaction)
                        send_kash.notify_recipient(recipient, amount)
                    total_amount += amount
                if (total_amount + send_kash.fees) < send_kash.total:
                    fee_txn.amount += (send_kash.total - (total_amount + send_kash.fees))

            elif send_kash.group_mode == SendKash.GroupMode.pacha:
                for recipient in send_kash.recipients.all():
                    transaction = send_to_recipient(recipient, send_kash, send_kash.amount.amount)
                    if transaction.status == TransactionStatusEnum.success.value:
                        send_kash.record_transaction(recipient, send_kash.amount, txn, transaction)
                        send_kash.notify_recipient(recipient, send_kash.amount.amount)
            elif send_kash.group_mode == SendKash.GroupMode.faro:
                r = [random.randint(1, 9) for i in range(0, recipient_count)]
                weights = [i / sum(r) for i in r]
                total_amount = Money(0, "XOF")
                for index, recipient in enumerate(send_kash.recipients.all()):
                    amount = round(send_kash.amount * weights[index]) - Money(1, "XOF")
                    transaction = send_to_recipient(recipient, send_kash, amount)
                    if transaction.status == TransactionStatusEnum.success.value:
                        send_kash.record_transaction(recipient, amount, txn, transaction)
                        send_kash.notify_recipient(recipient, amount)
                    total_amount += amount
                if (total_amount + send_kash.fees) < send_kash.total:
                    fee_txn.amount += (send_kash.total - (total_amount + send_kash.fees))
            else:
                raise NotImplemented()
        if fee_txn.amount.amount > 0:
            fee_txn.save()
