from decimal import Decimal

from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money
from rest_framework.decorators import api_view
from rest_framework.response import Response

from kash.utils import Conversions, StellarHelpers


@api_view(http_method_names=['GET'])
def version(request):
    return Response({
        'version': "1.1.0",
        'ios_url': "http://kashafrica.app.link/EKgDUkI0Hfb",
        'android_url': "http://kashafrica.app.link/EKgDUkI0Hfb",
        'url': "http://kashafrica.app.link/EKgDUkI0Hfb",
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
            "XOF": Conversions.get_xof_usd_deposit_rate()
        },
        "transfer": {
            "USD": 1,
            "XOF": Conversions.get_xof_usd_deposit_rate()
        }
    })

