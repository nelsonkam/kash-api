from decimal import Decimal

from django.http import Http404
from djmoney.money import Money
from rest_framework.decorators import action
from rest_framework.exceptions import Throttled
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.models import Transaction, Wallet, UserProfile, WalletFundingHistory
from kash.pagination import KashPagination
from kash.serializers.wallet import WalletSerializer
from kash.throttles import DepositRateThrottle
from kash.utils import StellarHelpers, TransactionStatusEnum, TransactionType, Conversions


class WalletViewSet(ReadOnlyModelViewSet):
    serializer_class = WalletSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "external_id"
    pagination_class = KashPagination

    def get_queryset(self):
        return Wallet.objects.filter(profile=self.request.user.profile)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        if self.kwargs[lookup_url_kwarg] == "current":
            if hasattr(self.request.user.profile, 'wallet'):
                obj = self.request.user.profile.wallet
            else:
                raise Http404
        else:
            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True, methods=["POST"])
    def deposit(self, request, external_id=None):
        wallet = self.get_object()
        amount = Decimal(request.data.get("amount"))
        xof_amount = Money(amount, request.data.get('currency'))
        phone = request.data.get('phone')
        gateway = request.data.get('gateway')
        txn = Transaction.objects.request(**{
            'obj': wallet,
            'name': wallet.profile.name,
            'amount': xof_amount,
            'phone': phone,
            'gateway': gateway,
            'initiator': wallet.profile.user
        })
        WalletFundingHistory.objects.create(
            txn_ref=txn.reference,
            wallet=wallet,
            status=WalletFundingHistory.FundingStatus.pending
        )
        return Response({'txn_ref': txn.reference})

    @action(detail=True, methods=["POST"])
    def withdraw(self, request, external_id=None):
        wallet = self.get_object()
        currency = request.data.get('currency', "USD")
        if currency.upper() == "USD":
            payout_method = wallet.profile.momo_accounts.first()
            amount = Money(request.data.get('amount'), request.data.get('currency', "USD"))
            wallet.withdraw(amount, payout_method.phone, payout_method.gateway)
        elif currency.upper() == "XOF":
            amount = request.data.get('amount')
            amount = Money(round(Decimal(amount) / Conversions.get_usd_rate(), 7), "USD")
            wallet.withdraw(amount, request.data.get('phone'), request.data.get('gateway'))

        return Response(status=200)

    @action(detail=True, methods=["POST"])
    def transfer(self, request, external_id=None):
        wallet = self.get_object()
        tags = request.data.get("recipient_tags")
        profiles = UserProfile.objects.filter(kashtag__in=tags)
        nowallet_profiles = profiles.filter(wallet__isnull=True)
        if nowallet_profiles.count() > 0:
            raise Exception("Some recipients do not have kash wallets for transfer.")
        wallets = Wallet.objects.filter(profile__kashtag__in=tags)
        wallet.bulk_transfer(wallets, Money(request.data.get("amount"), "USD"), request.data.get("note"))
        return Response(status=200)
