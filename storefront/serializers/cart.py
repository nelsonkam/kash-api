from djmoney.money import Money
from rest_framework import serializers

from core.models import Cart, CartItem, Product
from core.serializers.base import BaseModelSerializer
from core.utils import money_to_dict
from storefront.serializers.product import ProductSerializer


class CartItemSerializer(BaseModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["quantity", "product", "id", "price", "price_currency"]


class CartItemInputSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(min_value=0)
    product_id = serializers.IntegerField()


class CartSerializer(BaseModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    cart_items = CartItemInputSerializer(many=True, write_only=True)
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return money_to_dict(obj.total)

    def save_items(self, cart, items):
        cart.items.all().delete()
        products = Product.objects.filter(pk__in=[item.get("product_id") for item in items]).all()
        products = list(products)
        for item in items:
            if item.get("quantity", 0) != 0:
                product = filter(lambda i: i.id == item.get("product_id"), products)[0]
                CartItem.objects.create(
                    **{
                        "quantity": item.get("quantity"),
                        "product_id": item.get("product_id"),
                        "cart_id": cart.id,
                        "price": product.price
                    },
                )

    def create(self, validated_data):
        cart = Cart.objects.create(shop=validated_data.get('shop'))
        self.save_items(cart, validated_data.get("cart_items"))
        return cart

    def update(self, instance, validated_data):
        self.save_items(instance, validated_data.get("cart_items"))
        return instance

    class Meta:
        model = Cart
        fields = ["uid", "created_at", "items", "cart_items", "paid", "total"]
