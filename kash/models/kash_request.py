from django.db import models
from djmoney.models.fields import MoneyField

from core.models.base import BaseModel


class KashRequest(BaseModel):
    recipients = models.ManyToManyField('kash.UserProfile', related_name='kash_requests')
    initiator = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE, related_name='kash_requested')
    note = models.TextField()
    amount = MoneyField(max_digits=17, decimal_places=2, default_currency='XOF')

    def notify_recipients(self):
        from kash.models import Notification

        amount = self.amount.amount
        # sender_name = "Quelqu'un" if self.is_incognito else f"${self.initiator.kashtag}"
        sender_name = f"${self.initiator.kashtag}"
        for recipient in self.recipients.all():
            notif = Notification.objects.create(
                title="Besoin de kash 💰",
                description=f"{sender_name} a besoin de {amount} FCFA pour \"{self.note}\"",
                content_object=self,
                profile=recipient
            )
            notif.send()


class KashRequestResponse(BaseModel):
    sender = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE, related_name='request_responses')
    request = models.ForeignKey(KashRequest, on_delete=models.CASCADE, related_name='responses')
    accepted = models.BooleanField()
    transaction = models.ForeignKey('kash.KashTransaction', on_delete=models.CASCADE, null=True)
