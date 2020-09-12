from core.models import Category
from core.serializers.base import BaseModelSerializer
from storefront.serializers import ProductSerializer


class CategorySerializer(BaseModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "products",
        ]

        depth = 2
