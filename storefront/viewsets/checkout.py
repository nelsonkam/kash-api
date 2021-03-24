from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import Checkout, Order, CartItem
from core.utils.payment import Payment
from core.viewsets.base import CreateRetrieveUpdateViewSet
from storefront.serializers import CheckoutSerializer


class CheckoutViewSet(CreateRetrieveUpdateViewSet):
    serializer_class = CheckoutSerializer
    permission_classes = [AllowAny]
    lookup_field = "uid"
    queryset = Checkout.objects.all()

    @action(detail=True, methods=['post'])
    def pay(self, request, uid=None):
        checkout = self.get_object()
        if request.data.get("shipping"):
            checkout.shipping_profile_id = request.data.get("shipping").get('profile_id')
            price = request.data.get("shipping").get('rate').get('price')
            checkout.shipping_fees = convert_money(Money(price.get('amount'), price.get('currency')), checkout.shop.currency_iso)
            checkout.save()
        checkout.payment_method = request.data.get("payment_method")
        checkout.save()
        data = Payment.create_transaction(checkout, checkout.payment_method, **request.data)
        return Response(data)

    @action(detail=True, methods=['post'])
    def paid(self, request, uid):
        checkout = self.get_object()
        checkout.pay(**request.data)

        return Response(self.get_serializer(checkout).data)

    @action(detail=True)
    def shipping(self, request, uid=None):
        checkout = self.get_object()
        zone = request.query_params.get("zone")
        profiles = checkout.shop.shippingprofile_set.filter(zones__name=zone)
        return Response(
            {'options': [{
                'id': profile.pk,
                'name': profile.name,
                'logo': profile.avatar_url,
                'zone': zone,
                'rates': profile.get_rates(zone, origin=checkout.shop.country_code, items=checkout.cart.items.all())
            }] for profile in profiles}
        )


