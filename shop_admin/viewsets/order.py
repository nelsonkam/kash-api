from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Order
from shop_admin.permissions import IsCurrentShopOwner
from shop_admin.serializers.order import OrderSerializer
from shop_admin.viewsets.base import BaseModelViewSet


class OrderViewSet(BaseModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCurrentShopOwner]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        # return self.request.shop.order_set.all()
        return Order.objects.all()
