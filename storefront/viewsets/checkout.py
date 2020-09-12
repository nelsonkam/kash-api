from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from core.models import Checkout
from storefront.serializers import CheckoutSerializer


class CheckoutViewSet(ModelViewSet):
    serializer_class = CheckoutSerializer
    permission_classes = [AllowAny]
    lookup_field = "uid"
    queryset = Checkout.objects.all()
