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
            checkout.shipping_option = request.data.get("shipping")
            checkout.save()

        data = Payment.create_transaction(checkout, checkout.payment_method)
        return Response(data)

    @action(detail=True, methods=['post'])
    def paid(self, request, uid):
        checkout = self.get_object()
        if not checkout.paid and Payment.verify_transaction(**request.data):
            cart = checkout.cart
            for shop in cart.shops.all():
                order = Order.objects.create(
                    customer=checkout.customer,
                    country=checkout.country,
                    city=checkout.city,
                    address=checkout.address,
                    shipping_option=checkout.shipping_option,
                    payment_method=checkout.payment_method,
                    shop=shop
                )
                items = CartItem.objects.filter(cart=cart, product__shop=shop).select_related("product").all()
                for item in items:
                    order.items.create(quantity=item.quantity, product=item.product)
                order.notify_shop()
            checkout.paid = True
            checkout.save()

        return Response(self.get_serializer(checkout).data)

    @action(detail=True)
    def shipping(self, request, uid=None):
        checkout = self.get_object()
        if checkout.country.lower() == "benin":
            if "cotonou" in checkout.city.lower():
                return Response(
                    [
                        {
                            "name": "Futurix Logistic",
                            "price": {"amount": 1000, "currency": "XOF"},
                            "eta": "1-2 jours",
                        }
                    ]
                )
            elif "calavi" in checkout.city.lower():
                return Response(
                    [
                        {
                            "name": "Futurix Logistic",
                            "price": {"amount": 1500, "currency": "XOF"},
                            "eta": "1-2 jours",
                        }
                    ]
                )
            else:
                return Response(
                    [
                        {
                            "name": "Futurix Logistic",
                            "price": {"amount": 2500, "currency": "XOF"},
                            "eta": "2-3 jours",
                        }
                    ]
                )
        else:
            weight = 0
            for item in checkout.cart.items.all().select_related("product"):
                weight += (item.product.weight or 1) * item.quantity
            return Response(
                [
                    {
                        "name": "Futurix Logistic",
                        "price": {"amount": 22000 + (8000 * (weight - 2)), "currency": "XOF"},
                        "eta": "7-14 jours",
                    }
                ]
            )