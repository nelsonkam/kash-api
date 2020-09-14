from rest_framework.fields import SerializerMethodField

from core.models import Order, OrderItem
from core.serializers.base import BaseModelSerializer


class OrderItemSerializer(BaseModelSerializer):

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "total", "created_at"]
        depth = 1


class OrderSerializer(BaseModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "country",
            "city",
            "address",
            "shipping_option",
            "shipping_fees",
            "ref_id",
            "payment_method",
            "items",
            "shop",
            "total",
            "commission",
            "earnings",
            "created_at",
        ]
        depth = 2
