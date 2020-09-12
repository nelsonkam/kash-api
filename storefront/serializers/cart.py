from rest_framework import serializers

from core.models import Cart, CartItem
from core.serializers.base import BaseModelSerializer
from storefront.serializers.product import ProductSerializer


class CartItemSerializer(BaseModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["quantity", "product", "id"]


class CartItemInputSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(min_value=0)
    product_id = serializers.IntegerField()


class CartSerializer(BaseModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    cart_items = CartItemInputSerializer(many=True, write_only=True)
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return obj.total()

    def save_items(self, cart, items):
        for item in items:
            print(item)
            cart_item, created = CartItem.objects.update_or_create(
                pk=item.get("id"),
                defaults={
                    "quantity": item.get("quantity"),
                    "product_id": item.get("product_id"),
                    "cart_id": cart.id,
                },
            )

            if item.get("quantity", 0) == 0:
                cart_item.delete()

    def create(self, validated_data):
        cart = Cart.objects.create()
        self.save_items(cart, validated_data.get("cart_items"))
        return cart

    def update(self, instance, validated_data):
        self.save_items(instance, validated_data.get("cart_items"))
        return instance

    class Meta:
        model = Cart
        fields = ["uid", "created_at", "items", "cart_items", "total"]
