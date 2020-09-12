import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Product, Shop
from core.utils import upload_base64
from shop_admin.permissions import IsCurrentShopOwner
from shop_admin.serializers.product import ProductSerializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsCurrentShopOwner]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return self.request.shop.products.all()

    def perform_create(self, serializer):
        shop = get_object_or_404(Shop, pk=self.request.data.get("shop_id"))
        serializer.save(shop=shop)

    @action(detail=True, methods=["post"])
    def upload_images(self, request, pk=None):
        images = request.data.get("images", [])
        product = self.get_object()
        for image in images:
            url = upload_base64(image)
            product.images.create(url=url)

        return Response(ProductSerializer(instance=product).data)
