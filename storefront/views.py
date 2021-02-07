from urllib.parse import urlparse

from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import Banner, Category, Product, Shop
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

def index(request):
    host = request.headers['host'].split(':')[0]
    context = {
        'shop': get_object_or_404(Shop, domains__contains=[host]),
    }
    return render(request, 'storefront/index.html', context)

def product_details(request, slug=None):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product,
        'shop': product.shop
    }
    return render(request, 'storefront/product.html', context)
