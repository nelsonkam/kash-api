from core.models import Product
from core.serializers.base import BaseModelSerializer


class ProductSerializer(BaseModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'price', 'currency_iso', 'slug', 'description', 'category', 'shop', 'images']
        depth = 1
