from uuid import uuid4

from django.core.files import File
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Shop
from core.utils import upload_content_file
from shop_admin.serializers.shop import ShopSerializer


class ShopViewSet(ModelViewSet):
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = [JSONParser, MultiPartParser]

    @action(detail=True, methods=['post'])
    def avatar(self, request, pk=None):
        shop = self.get_object()
        image = request.data['avatar']
        shop.avatar_url = upload_content_file(image, f"{uuid4()}-{image.name}")
        shop.save()
        return Response(self.get_serializer(instance=shop).data)

    @action(detail=True, methods=['post'])
    def cover(self, request, pk=None):
        shop = self.get_object()
        image = request.data['cover']
        shop.cover_url = upload_content_file(image, f"{uuid4()}-{image.name}")
        shop.save()
        return Response(self.get_serializer(instance=shop).data)

    def get_queryset(self):
        return self.request.user.shops.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
