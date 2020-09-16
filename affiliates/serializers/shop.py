from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from core.models import Shop
from storefront.serializers import ProductSerializer


class ShopSerializer(ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    affiliate_earnings = SerializerMethodField(read_only=True)

    def get_affiliate_earnings(self, shop):
        return sum([order.affiliate_earnings for order in shop.orders.all()])

    class Meta:
        model = Shop
        fields = [
            "id",
            "username",
            "name",
            "avatar_url",
            "whatsapp_number",
            "description",
            "phone_number",
            "products",
            "cover_url",
            "affiliate_earnings",
            "order_count"
        ]
        depth = 2
