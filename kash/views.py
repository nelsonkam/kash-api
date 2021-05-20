from decimal import Decimal

from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money
from rest_framework.decorators import api_view
from rest_framework.response import Response

from kash.utils import Conversions, StellarHelpers


@api_view(http_method_names=['GET'])
def version(request):
    return Response({
        'version': "1.0.0",
        'ios_url': "https://apple.com"
    })


@api_view(http_method_names=['GET'])
def rates(request):
    return Response({
        "deposit": {
            "USD": 1,
            "XOF": Conversions.get_xof_usd_deposit_rate()
        },
        "withdraw": {
            "USD": 1,
            "XOF": Conversions.get_xof_usd_withdrawal_rate()
        },
        "transfer": {
            "USD": 1,
            "XOF": round(convert_money(Money(1, "USD"), "XOF").amount)
        }
    })

