from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import Shop, Cart
from pay.models import CheckoutSession
from storefront.serializers import ShopSerializer, CartSerializer


class CheckoutSessionSerializer(ModelSerializer):
    shop = ShopSerializer(read_only=True)
    cart = CartSerializer(read_only=True)
    shop_domain = serializers.CharField(write_only=True)
    cart_id = serializers.CharField(write_only=True)

    def create(self, validated_data):
        shop_domain = validated_data.pop('shop_domain')
        cart_id = validated_data.pop('cart_id')
        shop = Shop.objects.filter(domains__contains=[shop_domain]).first()
        cart = Cart.objects.filter(uid=cart_id).first()
        return CheckoutSession.objects.create(shop=shop, cart=cart, **validated_data)

    class Meta:
        model = CheckoutSession
        fields = ['session_id', 'created_at', 'shop', 'cart', 'cancel_url', 'shop_domain', 'cart_id']

class ShippingOptionSerializer(serializers.Serializer):
    profile_id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    price_amount = serializers.CharField()
    price_currency = serializers.CharField()

    class Meta:
        fields = ['profile_id', 'name', 'description', 'price_amount', 'price_currency']


class CheckoutSessionPaymentSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    delivery_zone = serializers.CharField()
    address_details = serializers.CharField()
    customer_name = serializers.CharField(required=False)
    payment_method = serializers.CharField()
    payment_payload = serializers.DictField(required=False)
    shipping_option = ShippingOptionSerializer()

    class Meta:
        fields = ['user_id', 'delivery_zone', 'address_details', 'customer_name', 'payment_gateway', 'payment_phone', 'shipping_option']
