from rest_framework import serializers

from core.models import Product, ProductImage
from core.serializers.base import BaseModelSerializer


class ProductImageSerializer(BaseModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "product", "url")


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
