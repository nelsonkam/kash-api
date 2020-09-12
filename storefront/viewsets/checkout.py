from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import Checkout
from core.utils.payment import Payment
from core.viewsets.base import CreateRetrieveUpdateViewSet
from storefront.serializers import CheckoutSerializer


class CheckoutViewSet(CreateRetrieveUpdateViewSet):
    serializer_class = CheckoutSerializer
    permission_classes = [AllowAny]
    lookup_field = "uid"
    queryset = Checkout.objects.all()

    @action(detail=True)
    def pay(self, request, uid=None):
        checkout = self.get_object()
        if request.data.get("shipping"):
            checkout.shipping_option = request.data.get("shipping")
            checkout.save()

        transaction = Payment.create_transaction(checkout)
        token = Payment.create_payment_token(transaction.get("id"))
        return {"payment_url": token.get("url")}

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
            return Response(
                [
                    {
                        "name": "Futurix Logistic",
                        "price": {"amount": 21000, "currency": "XOF"},
                        "eta": "7-14 jours",
                    }
                ]
            )
