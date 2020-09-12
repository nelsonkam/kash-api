from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Shop
from shop_admin.serializers.shop import ShopSerializer


class ShopViewSet(ModelViewSet):
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return self.request.user.shops.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
