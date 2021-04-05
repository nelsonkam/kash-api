from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now
from onesignal_sdk.client import Client

from core.models.base import BaseModel


class Notification(BaseModel):
    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    content_object = GenericForeignKey('content_type', 'object_id')
    profile = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    description = models.TextField()
    sent_at = models.DateTimeField(null=True)

    def send(self):
        client = Client(app_id=settings.ONESIGNAL_APP_ID, rest_api_key=settings.ONESIGNAL_REST_API_KEY)

        notification_body = {
            'headings': {'en': self.title},
            'contents': {'en': self.description},
            'include_player_ids': self.profile.device_ids
        }
        response = client.send_notification(notification_body)
        if response.status_code == 200 and response.body['recipients'] > 0:
            self.sent_at = now()
            self.save()