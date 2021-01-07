from urllib.parse import urlparse

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.models import Shop
from storefront.serializers import ShopSerializer


class ShopViewSet(ReadOnlyModelViewSet):
    serializer_class = ShopSerializer
    permission_classes = [AllowAny]
    lookup_field = "username"
    queryset = Shop.objects.all()

    def get_object(self):
        lookup_field_val = self.kwargs[self.lookup_field]
        if lookup_field_val == "current":
            origin = urlparse(self.request.headers['origin'])
            obj = get_object_or_404(Shop, domains__contains=[origin.hostname])
            self.check_object_permissions(self.request, obj)
            return obj
        else:
            return super().get_object()

