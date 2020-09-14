import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers

from core.models import Shop
from core.serializers.base import BaseModelSerializer
from core.utils import upload_base64


class ShopSerializer(BaseModelSerializer):

    class Meta:
        model = Shop
        fields = [
            "name",
            "username",
            "avatar_url",
            "whatsapp_number",
            "description",
            "phone_number",
            "user",
            "products",
            "balance",
            "order_count",
            "cover_url",
            "id"
        ]
        depth = 1
