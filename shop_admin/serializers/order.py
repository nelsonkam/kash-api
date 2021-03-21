from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from core.models import Order, OrderItem
from core.serializers.base import BaseModelSerializer
from core.utils import money_to_dict


class OrderItemSerializer(BaseModelSerializer):
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return money_to_dict(obj.total)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "total", "created_at"]
        depth = 1


class OrderSerializer(BaseModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    commission = serializers.SerializerMethodField()
    earnings = serializers.SerializerMethodField()

    def get_total(self, obj):
        return money_to_dict(obj.total)

    def get_commission(self, obj):
        return money_to_dict(obj.commission)

    def get_earnings(self, obj):
        return money_to_dict(obj.earnings)

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
