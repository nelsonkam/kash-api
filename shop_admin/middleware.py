from django.http import HttpRequest

from core.models import User, Shop


class ShopMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        shop_id = request.META.get("HTTP_X_SHOP_ID", None)
        request.shop = None if not shop_id else Shop.objects.filter(pk=shop_id).first()
        response = self.get_response(request)
        return response
