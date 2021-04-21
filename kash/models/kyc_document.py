from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models.base import BaseModel
from django.db import models

from core.utils.notify import tg_bot
from kash.signals import transaction_status_changed


class KYCDocument(BaseModel):
    class IDDocType(models.TextChoices):
        id_card = "id_card"
        passport = "passport"

    class Status(models.TextChoices):
        pending = "pending"
        approved = "approved"
        rejected = "rejected"

    doc_url = models.URLField(null=True)
    document_type = models.CharField(max_length=25)
    selfie_url = models.URLField(null=True)
    profile = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.pending)

    @property
    def name(self):
        name_map = {
            'id_card': "Carte d'identité",
            'passport': "Passeport"
        }
        return name_map[self.document_type]

@receiver(post_save, sender=KYCDocument)
def notify(sender, instance, created, **kwargs):
    if created:
        tg_bot.send_message(chat_id=settings.TG_CHAT_ID, text=f"""
New KYC Document on Kash!💪🏾

{"_Ceci est un message test._" if settings.DEBUG else ""}
""")
