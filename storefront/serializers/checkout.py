from rest_framework import serializers

from core.models import Checkout, Customer, Cart
from core.serializers.base import BaseModelSerializer
from storefront.serializers.cart import CartSerializer


class CheckoutSerializer(BaseModelSerializer):
    cart = CartSerializer(read_only=True)
    contact = serializers.CharField()

    def create(self, validated_data):
        contact = validated_data.pop("contact")
        if "@" in contact:
            customer = Customer.objects.get_or_create(
                email=contact, defaults={"name": validated_data.pop("name")}
            )
        else:
            customer = Customer.objects.get_or_create(
                phone_number=contact, defaults={"name": validated_data.pop("name")}
            )
        cart_uid = validated_data.pop('cart_uid')
        checkout = Checkout(**validated_data)
        checkout.customer = customer
        checkout.cart = Cart.objects.get(uid=cart_uid)
        checkout.save()
        return checkout


    class Meta:
        model = Checkout
        fields = [
            "id",
            "customer",
            "cart",
            "country",
            "city",
            "address",
            "uid",
            "shipping_option",
        ]
        depth = 1
