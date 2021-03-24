from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Order
from shop_admin.permissions import IsCurrentShopOwner
from shop_admin.serializers.order import OrderSerializer
from shop_admin.viewsets.base import BaseModelViewSet


class OrderViewSet(BaseModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.request.shop.orders.all().order_by("-created_at")
