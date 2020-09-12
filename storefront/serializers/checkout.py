from rest_framework import serializers

from core.models import Checkout, Customer, Cart
from core.serializers.base import BaseModelSerializer
from storefront.serializers.cart import CartSerializer


class CheckoutSerializer(BaseModelSerializer):
    cart = CartSerializer(read_only=True)
    name = serializers.CharField(write_only=True)
    contact = serializers.CharField(write_only=True)
    cart_uid = serializers.CharField(write_only=True)

    def create(self, validated_data):
        contact = validated_data.pop("contact")
        if "@" in contact:
            customer, created = Customer.objects.get_or_create(
                email=contact, defaults={"name": validated_data.pop("name")}
            )
        else:
            customer, created = Customer.objects.get_or_create(
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
            "contact",
            "name",
            "cart_uid"
        ]
        depth = 1
