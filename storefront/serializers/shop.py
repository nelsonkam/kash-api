from rest_framework.serializers import ModelSerializer

from core.models import Shop
from storefront.serializers import ProductSerializer


class ShopSerializer(ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = [
            'id',
            'username',
            'name',
            'avatar_url',
            'whatsapp_number',
            'description',
            'phone_number',
            "products"
        ]
        depth = 2
