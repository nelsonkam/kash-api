from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from djmoney.models.fields import MoneyField

from core.models.base import BaseModel



class KashTransaction(BaseModel):
    class TxnType(models.TextChoices):
        credit = "credit"
        debit = "debit"
    amount = MoneyField(max_digits=17, decimal_places=2, default_currency="XOF")
    sender = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE, related_name='txn_sent')
    receiver_id = models.IntegerField(null=True)
    receiver_type = models.ForeignKey(ContentType, null=True, on_delete=models.PROTECT)
    receiver = GenericForeignKey('receiver_type', 'receiver_id')
    profile = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE, related_name='kash_transactions')
    txn_ref = models.CharField(max_length=20, unique=True)
    txn = models.ForeignKey('kash.Transaction', on_delete=models.CASCADE)
    narration = models.TextField(blank=True)
    txn_type = models.CharField(max_length=20, choices=TxnType.choices)
    timestamp = models.DateTimeField(null=True)

    @property
    def status(self):
        from kash.models import Transaction
        return Transaction.objects.get(reference=self.txn_ref).status
