from django.conf import settings
from django.core import signing
from django.core.signing import BadSignature
from django.http import HttpResponseBadRequest
from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Order, Customer, User
from core.viewsets.base import CreateRetrieveUpdateViewSet
from kash.models import CheckoutSession
from kash.serializers.session import CheckoutSessionSerializer, CheckoutSessionPaymentSerializer


class SessionPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in ('GET', 'HEAD', 'OPTIONS', 'POST') or
            request.user and
            request.user.is_authenticated
        )


class CheckoutSessionViewset(CreateRetrieveUpdateViewSet):
    serializer_class = CheckoutSessionSerializer
    permission_classes = [SessionPermission]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'uid'

    def get_queryset(self):
        return CheckoutSession.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        session_id = self.kwargs[lookup_url_kwarg]
        try:
            data = signing.loads(session_id, max_age=3600)
        except BadSignature as exc:
            raise ValidationError(detail={'message': "Invalid session"})
        obj = get_object_or_404(queryset, pk=data.get('id'))
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True)
    def shipping(self, request, uid=None):
        session = self.get_object()
        zone = request.query_params.get("zone")
        profiles = session.shop.shippingprofile_set.filter(zones__name=zone)
        return Response(
            {'options': [{
                'id': profile.pk,
                'name': profile.name,
                'logo': profile.avatar_url,
                'zone': zone,
                'rates': profile.get_rates(zone, origin=session.shop.country_code, items=session.cart.items.all())
            }] for profile in profiles}
        )

    @action(detail=True, methods=['post'])
    def pay(self, request, uid=None):
        session = self.get_object()
        serializer = CheckoutSessionPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not hasattr(session, 'order'):
            session.order = Order()
        order = session.order
        order.shop = session.shop
        session.user = get_object_or_404(User, pk=serializer.validated_data['user_id'])
        if not session.user.name:
            session.user.name = serializer.validated_data['customer_name']
            session.user.save()
        customer, created = Customer.objects.get_or_create(phone=session.user.phone_number,
                                                           defaults={'name': session.user.name})
        order.customer = customer
        order.address = serializer.validated_data['address_details']
        order.payment_method = serializer.validated_data['payment_method']
        shipping = serializer.validated_data['shipping_option']
        order.shipping_profile_id = shipping.get("profile_id")
        order.shipping_fees = convert_money(Money(shipping.get('price_amount'), shipping.get('price_currency')),
                                            session.shop.currency_iso)
        order.zone = serializer.validated_data['delivery_zone']
        order.save()
        for item in session.cart.items.all():
            order.items.create(quantity=item.quantity, product=item.product, price=item.price)
        session.save()

