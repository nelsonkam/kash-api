import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers

from core.models import Shop, AffiliateAgent
from core.serializers import UserSerializer
from core.serializers.base import BaseModelSerializer
from core.utils import upload_base64


class ShopSerializer(BaseModelSerializer):
    user = UserSerializer(read_only=True)
    affiliate_code = serializers.CharField(write_only=True, required=False, allow_null=True)

    def create(self, validated_data):
        shop = Shop.objects.create(**validated_data)
        shop.domains.append(f"{shop.username}.kweek.shop")
        shop.save()
        if hasattr(validated_data, 'affiliate_code'):
            affiliate_code = validated_data.pop("affiliate_code")
            if affiliate_code:
                shop.affiliate = AffiliateAgent.objects.filter(code=affiliate_code).first()
                shop.save()
        return shop

    class Meta:
        model = Shop
        fields = [
            "name",
            "username",
            "avatar_url",
            "currency_iso",
            "country_code",
            "description",
            "phone_number",
            "user",
            "products",
            "balance",
            "order_count",
            "cover_url",
            "affiliate_code",
            "id"
        ]
        depth = 1
