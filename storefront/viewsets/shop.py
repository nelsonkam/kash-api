from urllib.parse import urlparse

from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.models import Shop
from storefront.serializers import ShopSerializer


class ShopViewSet(ReadOnlyModelViewSet):
    serializer_class = ShopSerializer
    permission_classes = [AllowAny]
    lookup_field = "username"
    
    def get_queryset(self):
        origin = urlparse(self.request.headers['origin'])
        return Shop.objects.filter(domains__contains=[origin.hostname])

    def get_object(self):
        lookup_field_val = self.kwargs[self.lookup_field]
        if lookup_field_val == "current":
            if 'origin' in self.request.headers:
                origin = urlparse(self.request.headers['origin'])
                host = origin.hostname
            else:
                host = self.request.headers['host'].split(':')[0].lower()
            obj = get_object_or_404(Shop, domains__contains=[host])
            self.check_object_permissions(self.request, obj)
            return obj
        else:
            return super().get_object()

    @action(detail=True)
    def shipping_zones(self, request, username=None):
        shop = self.get_object()
        zones = shop.shippingprofile_set.filter(zones__isnull=False).values_list('zones__name', flat=True)
        return Response({'zones': zones})

