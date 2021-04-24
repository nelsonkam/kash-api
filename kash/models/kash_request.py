from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver
from django.utils.timezone import now
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from core.models.base import BaseModel
from kash.signals import transaction_status_changed
from kash.utils import TransactionStatusEnum, TransactionType


class KashRequest(BaseModel):
    recipient = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE, related_name='kash_requests')
    initiator = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE, related_name='kash_requested')
    note = models.TextField()
    amount = MoneyField(max_digits=17, decimal_places=2, default_currency='XOF')
    rejected_at = models.DateTimeField(null=True)
    accepted_at = models.DateTimeField(null=True)

    @property
    def fees(self):
        if self.amount < Money(5000, "XOF"):
            return Money(0, "XOF")
        else:
            return self.amount * 0.03

    @property
    def total(self):
        return self.amount + self.fees

    def notify_recipient(self):
        from kash.models import Notification

        amount = self.amount.amount
        # sender_name = "Quelqu'un" if self.is_incognito else f"${self.initiator.kashtag}"
        sender_name = f"${self.initiator.kashtag}"
        notif = Notification.objects.create(
            title="Besoin de kash 💰",
            description=f"{sender_name} a besoin de {amount} FCFA pour \"{self.note}\"",
            content_object=self,
            profile=self.recipient
        )
        notif.send()

    def accept(self, phone, gateway):
        from kash.models import Transaction
        return Transaction.objects.request(
            obj=self,
            name=self.recipient.name,
            amount=self.total,
            initiator=self.recipient.user,
            phone=phone,
            gateway=gateway
        )


class KashRequestResponse(BaseModel):
    sender = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE, related_name='request_responses')
    request = models.ForeignKey(KashRequest, on_delete=models.CASCADE, related_name='responses')
    accepted = models.BooleanField()
    transaction = models.ForeignKey('kash.SendKash', on_delete=models.CASCADE, null=True)


@receiver(transaction_status_changed)
def payout_recipient(sender, **kwargs):
    from kash.models import Transaction, KashTransaction

    txn = kwargs.pop("transaction")
    kash_request_type = ContentType.objects.get_for_model(KashRequest)

    if txn.content_type == kash_request_type and txn.status == TransactionStatusEnum.success.value:
        kash_request = txn.content_object
        if kash_request.accepted_at or kash_request.rejected_at:
            return
        request_initiator = kash_request.initiator
        KashTransaction.objects.create(
            amount=txn.amount,
            sender=txn.initiator.profile,
            receiver=request_initiator,
            profile=txn.initiator.profile,
            txn_ref=txn.reference,
            txn=txn,
            narration="Demande de kash 💰",
            txn_type=KashTransaction.TxnType.debit,
            timestamp=now()
        )
        payment_method = request_initiator.momo_accounts.filter(gateway=txn.gateway).first()
        if not payment_method:
            payment_method = request_initiator.momo_accounts.first()
        payout_txn = Transaction.objects.request(
            obj=kash_request,
            name=request_initiator.name,
            phone=payment_method.phone,
            gateway=payment_method.gateway,
            amount=kash_request.amount,
            initiator=txn.initiator,
            txn_type=TransactionType.payout
        )
        if payout_txn.status == TransactionStatusEnum.success.value:
            kash_request.accepted_at = now()
            kash_request.save()

            KashTransaction.objects.create(
                amount=kash_request.amount,
                sender=payout_txn.initiator.profile,
                receiver=request_initiator,
                profile=request_initiator,
                txn_ref=payout_txn.reference,
                txn=txn,
                narration="Demande de kash 💰",
                txn_type=KashTransaction.TxnType.credit,
                timestamp=now()
            )



