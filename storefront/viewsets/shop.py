from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.models import Shop
from storefront.serializers import ShopSerializer


class ShopViewSet(ReadOnlyModelViewSet):
    serializer_class = ShopSerializer
    permission_classes = [AllowAny]
    lookup_field = "username"
    queryset = Shop.objects.all()
