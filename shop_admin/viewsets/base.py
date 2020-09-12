from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from shop_admin.permissions import IsCurrentShopOwner


class BaseModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsCurrentShopOwner]
    authentication_classes = [JWTAuthentication]
