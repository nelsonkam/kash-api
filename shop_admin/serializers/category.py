from rest_framework import serializers

from core.models import Category
from core.serializers.base import BaseModelSerializer


class CategorySerializer(BaseModelSerializer):
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'slug', 'name', 'product_count']
