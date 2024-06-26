from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import format_html

from django.db import models

from kash.abstract.models import BaseModel
from kash.xlib.utils import create_presigned_url
from kash.xlib.utils.notify import notify_telegram, notify_slack
from kash.notification.models import Notification


class KYCDocument(BaseModel):
    class IDDocType(models.TextChoices):
        id_card = "id_card"
        passport = "passport"

    class Status(models.TextChoices):
        pending = "pending"
        approved = "approved"
        rejected = "rejected"

    class Meta:
        db_table = "kash_kycdocument"

    doc_url = models.URLField(blank=True, null=True)
    document_type = models.CharField(max_length=25)
    selfie_url = models.URLField(blank=True, null=True)
    profile = models.ForeignKey("kash_user.UserProfile", on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.pending)
    rejection_reason = models.TextField(blank=True)

    @property
    def name(self):
        name_map = {"id_card": "Carte d'identité", "passport": "Passeport"}
        return name_map[self.document_type]

    @property
    def document_img(self):
        img_url = "" if not self.doc_url else create_presigned_url(self.doc_url)
        return format_html('<img style="height: 500px; width: auto" src="{}">', img_url)

    @property
    def selfie_img(self):
        img_url = "" if not self.selfie_url else create_presigned_url(self.selfie_url)
        return format_html('<img style="height: 500px; width: auto" src="{}">', img_url)


@receiver(post_save, sender=KYCDocument)
def notify(sender, instance, created, **kwargs):
    if instance.doc_url and instance.selfie_url and instance.status == KYCDocument.Status.pending:
        notify_slack(
            {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Un nouveau document de KYC a été ajouté sur Kash:\n"
                            f"*<https://prod.mykash.africa/admin/kash_kyc/kycdocument/{instance.pk}/change/|Document KYC>* cc <@U022DVC7E5S>",
                        },
                    },
                ]
            }
        )


@receiver(post_save, sender=KYCDocument, dispatch_uid="kyc_notify_status")
def notify_status(sender, instance, created, **kwargs):
    kyc_doc_type = ContentType.objects.get_for_model(KYCDocument)
    if not Notification.objects.filter(object_id=instance.id, content_type__pk=kyc_doc_type.id):
        if instance.status == KYCDocument.Status.rejected:
            instance.profile.push_notify(
                "Pièce d'identité rejetée 🙅🏽‍",
                f'Ta pièce d\'identité a été rejetée. Réessaie en prenant en compte le problème suivant: "{instance.rejection_reason}"',
                instance,
            )
        elif instance.status == KYCDocument.Status.approved:
            instance.profile.push_notify(
                "Pièce d'identité vérifiée ✅",
                f"Ta pièce d'identité a été approuvée avec succès!",
                instance,
            )
