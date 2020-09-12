from rest_framework import serializers

from core.models import Product
from core.serializers.base import BaseModelSerializer


class ProductSerializer(BaseModelSerializer):
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "slug",
            "images",
            "name",
            "description",
            "price",
            "currency_iso",
            "shop",
            "weight",
            "available_units",
        )
        depth = 1
