from uuid import uuid4

from django.core.files import File
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Shop
from core.utils import upload_content_file
from core.utils.payment import rave_request
from shop_admin.serializers.bank_account import BankAccountSerializer
from shop_admin.serializers.shop import ShopSerializer


class ShopViewSet(ModelViewSet):
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = [JSONParser, MultiPartParser]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        if self.kwargs[lookup_url_kwarg] == "current":
            obj = self.request.shop
        else:
            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        return self.request.user.shops.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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

    @action(detail=True, methods=['post'])
    def banks(self, request, pk=None):
        shop = self.get_object()
        resp = rave_request("GET", f"/banks/{shop.country_code}")
        return Response(resp.json().get("data"))

    @action(detail=True, methods=['post', "get"])
    def payout(self, request, pk=None):
        shop = self.get_object()
        if request.method == "POST":
            if hasattr(shop, 'bankaccount'):
                serializer = BankAccountSerializer(data=request.data, instance=shop.bankaccount, partial=True)
            else:
                serializer = BankAccountSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(shop=shop)
            # shop.bankaccount.create_subaccount()
            return Response(serializer.data)

        if hasattr(shop, 'bankaccount'):
            serializer = BankAccountSerializer(instance=shop.bankaccount)
            return Response(serializer.data)
        else:
            raise Http404()
