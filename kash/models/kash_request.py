from djmoney.models.fields import MoneyField

from core.models.base import BaseModel
from django.db import models

from kash.tasks import send_push_notification


class KashRequest(BaseModel):
    recipients = models.ManyToManyField('kash.UserProfile', related_name='kash_requests')
    initiator = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE, related_name='kash_requested')
    note = models.TextField()
    amount = MoneyField(max_digits=17, decimal_places=2, default_currency='XOF')

    def notify_recipients(self):
        amount = self.amount.amount
        # sender_name = "Quelqu'un" if self.is_incognito else f"${self.initiator.kashtag}"
        sender_name = f"${self.initiator.kashtag}"
        for recipient in self.recipients.all():
            send_push_notification(recipient.id, "Besoin de kash 💰",
                                   f"{sender_name} a besoin de {amount} FCFA pour \"{self.note}\"",
                                   self)
