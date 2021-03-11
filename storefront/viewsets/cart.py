from urllib.parse import urlparse

from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

from core.models import Cart, Shop
from core.viewsets.base import CreateRetrieveUpdateViewSet
from storefront.serializers.cart import CartSerializer


class CartViewSet(CreateRetrieveUpdateViewSet):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    lookup_field = "uid"
    queryset = Cart.objects.all()

    def perform_create(self, serializer):
        origin = urlparse(self.request.headers['origin'])
        shop = get_object_or_404(Shop, domains__contains=[origin.hostname])
        serializer.save(shop=shop)
