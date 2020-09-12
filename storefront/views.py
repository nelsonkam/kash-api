from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import Banner, Category, Product
from storefront.serializers import ProductSerializer
from storefront.serializers.category import CategorySerializer


@api_view()
@permission_classes([AllowAny])
def feed(request):
    return Response(data={
        'banners': Banner.objects.values(),
        'categories': CategorySerializer(Category.objects.all(), many=True).data,
        'products': ProductSerializer(Product.objects.order_by("-created_at")[0:50], many=True).data
    })
