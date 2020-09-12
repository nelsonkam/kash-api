from django.db.models import Q
from rest_framework.fields import SerializerMethodField

from core.models import Product
from core.serializers.base import BaseModelSerializer


class SimilarProductSerializer(BaseModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "currency_iso",
            "slug",
            "description",
            "images",
        ]
        depth = 1


class ProductSerializer(BaseModelSerializer):
    similar = SerializerMethodField(read_only=True)

    def get_similar(self, product):
        return SimilarProductSerializer(product.similar, many=True).data

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "currency_iso",
            "slug",
            "description",
            "category",
            "shop",
            "images",
            "similar",
        ]
        depth = 1
