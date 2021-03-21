from rest_framework import serializers

from core.models import Checkout, Customer, Cart
from core.serializers.base import BaseModelSerializer
from core.utils import money_to_dict
from storefront.serializers.cart import CartSerializer


class CheckoutSerializer(BaseModelSerializer):
    cart = CartSerializer(read_only=True)
    name = serializers.CharField(write_only=True)
    contact = serializers.CharField(write_only=True)
    cart_uid = serializers.CharField(write_only=True)
    uid = serializers.CharField(read_only=True)
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return money_to_dict(obj.total)

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
            "shipping_fees",
            "shipping_fees_currency",
            "shipping_profile",
            "contact",
            "name",
            "cart_uid",
            "ref_id",
            "payment_method",
            "paid"
        ]
        depth = 1
