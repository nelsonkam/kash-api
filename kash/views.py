from djmoney.money import Money

from rest_framework.decorators import api_view
from rest_framework.response import Response

from kash.xlib.utils.notify import parse_command
from kash.xlib.utils.payment import rave_request
from kash.xlib.utils.utils import Conversions


@api_view(http_method_names=["GET"])
def version(request):
    return Response(
        {
            "version": "1.2.1",
            "ios_url": "http://kashafrica.app.link/EKgDUkI0Hfb",
            "ios": "http://kashafrica.app.link/EKgDUkI0Hfb",
            "android_url": "http://kashafrica.app.link/EKgDUkI0Hfb",
            "android": "http://kashafrica.app.link/EKgDUkI0Hfb",
            "url": "http://kashafrica.app.link/EKgDUkI0Hfb",
        }
    )


@api_view(http_method_names=["GET"])
def rates(request):
    return Response(
        {
            "deposit": {"USD": 1, "XOF": Conversions.get_usd_rate()},
            "withdraw": {"USD": 1, "XOF": Conversions.get_usd_rate()},
            "transfer": {"USD": 1, "XOF": Conversions.get_usd_rate()},
        }
    )


@api_view(http_method_names=["GET"])
def card_info(request):
    return Response(
        {
            "usd_rate": {
                "amount": Conversions.get_xof_from_usd(Money(1, "USD")).amount,
                "currency": "XOF",
            },
            "minimum_deposit": {"amount": 5, "currency": "USD"},
            "fees": {
                "transaction": {"amount": 0, "is_percentage": True},
                "withdrawal": {"amount": 3, "is_percentage": True},
                "issuing": {"amount": 0, "currency": "FCFA"},
            },
        }
    )


@api_view(http_method_names=["GET"])
def recharge(request):
    ngn_balance = (
        rave_request("GET", "/balances/NGN").json().get("data").get("available_balance")
    )
    usd_balance = (
        rave_request("GET", "/balances/USD").json().get("data").get("available_balance")
    )
    data = rave_request("GET", f"/rates?from=NGN&to=USD&amount={ngn_balance}").json()
    amount = data.get("data").get("to").get("amount")
    amount_to_charge = 1000 - (usd_balance + amount)
    return Response({"amount_to_fund": amount_to_charge})


@api_view(http_method_names=["POST"])
def tg_bot(request):
    parse_command(request.data)
    return Response(status=200)
