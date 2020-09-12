import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers

from core.models import Shop
from core.serializers.base import BaseModelSerializer
from core.utils import upload_base64


class ShopSerializer(BaseModelSerializer):
    avatar_uri = serializers.CharField(write_only=True)

    def create(self, validated_data):
        avatar_uri = validated_data.pop("avatar_uri")
        url = upload_base64(avatar_uri)
        shop = Shop(**validated_data)
        shop.avatar_url = url
        shop.save()
        return shop

    class Meta:
        model = Shop
        fields = [
            "name",
            "username",
            "avatar_url",
            "avatar_uri",
            "whatsapp_number",
            "description",
            "phone_number",
            "user",
            "products",
            "id"
        ]
        depth = 1
