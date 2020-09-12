from rest_framework.permissions import AllowAny

from core.models import Cart
from core.viewsets.base import CreateRetrieveUpdateViewSet
from storefront.serializers.cart import CartSerializer


class CartViewSet(CreateRetrieveUpdateViewSet):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    lookup_field = "uid"
    queryset = Cart.objects.all()
