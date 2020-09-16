from affiliates.serializers import OrderSerializer
from affiliates.viewsets.base import AffiliatesBaseModelViewSet
from core.models import Order


class OrderViewSet(AffiliatesBaseModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(shop__affiliate=self.request.user.affiliate)
