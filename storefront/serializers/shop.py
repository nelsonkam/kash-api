from rest_framework.serializers import ModelSerializer

from core.models import Shop
from storefront.serializers import ProductSerializer


class ShopSerializer(ModelSerializer):

    class Meta:
        model = Shop
        fields = [
            "id",
            "username",
            "name",
            "avatar_url",
            "description",
            "phone_number",
            "cover_url",
        ]
