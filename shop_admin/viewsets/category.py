from rest_framework.generics import get_object_or_404

from core.models import Shop
from shop_admin.serializers.category import CategorySerializer
from shop_admin.viewsets.base import BaseModelViewSet


class CategoryViewSet(BaseModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return self.request.shop.category_set.all()

    def perform_create(self, serializer):
        shop = get_object_or_404(Shop, pk=self.request.shop.pk)
        serializer.save(shop=shop)
