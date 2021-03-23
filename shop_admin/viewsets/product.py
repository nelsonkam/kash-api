import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Product, Shop, ProductImage, Category
from core.utils import upload_base64, upload_content_file
from shop_admin.permissions import IsCurrentShopOwner
from shop_admin.serializers.product import ProductSerializer, ProductImageSerializer
from shop_admin.viewsets.base import BaseModelViewSet


class ProductViewSet(BaseModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsCurrentShopOwner]
    authentication_classes = [JWTAuthentication]
    parser_classes = [JSONParser, MultiPartParser]

    def get_queryset(self):
        return self.request.shop.products.all()

    def perform_create(self, serializer):
        shop = get_object_or_404(Shop, pk=self.request.data.get("shop_id"))
        serializer.save(shop=shop)

    @action(detail=True, methods=["post"])
    def upload_images(self, request, pk=None):
        images = request.FILES.getlist("images")
        product = self.get_object()
        for image in images:
            url = upload_content_file(image, f"{uuid.uuid4()}-{image.name}")
            product.images.create(url=url)

        return Response(ProductSerializer(instance=product).data)

    @action(detail=True, methods=['post'])
    def categories(self, request, pk=None):
        product = self.get_object()
        categories = request.data.get("categories")
        product.categories.set(Category.objects.filter(pk__in=categories).all())
        return Response(self.get_serializer(instance=product).data)


class ProductImageViewSet(BaseModelViewSet):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product__shop=self.request.shop).all()
