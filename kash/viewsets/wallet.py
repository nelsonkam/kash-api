from djmoney.money import Money
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.models import Transaction
from kash.serializers.wallet import WalletSerializer, WalletTransactionSerializer
from kash.pagination import KashPagination
from kash.utils import Conversions


class WalletViewSet(ReadOnlyModelViewSet):
    serializer_class = WalletSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "balance_currency"
    pagination_class = KashPagination

    def get_queryset(self):
        return self.request.user.profile.wallets.all()

    @action(detail=True, methods=["GET"])
    def transactions(self, request, balance_currency=None):
        wallet = self.get_object()
        queryset = wallet.transactions.all().order_by("-timestamp")
        queryset = self.paginate_queryset(queryset)
        return self.get_paginated_response(WalletTransactionSerializer(queryset, many=True).data)

    @action(detail=True, methods=["POST"])
    def deposit(self, request, balance_currency=None):
        wallet = self.get_object()
        amount = Money(request.data.get('amount'), request.data.get('currency'))
        phone = request.data.get('phone')
        gateway = request.data.get('gateway')
        txn = Transaction.objects.request(**{
            'obj': wallet,
            'name': wallet.profile.name,
            'amount': amount,
            'phone': phone,
            'gateway': gateway,
            'initiator': wallet.profile.user
        })
        return Response({'txn_ref': txn.reference})

    @action(detail=True, methods=["POST"])
    def withdraw(self, request, balance_currency=None):
        wallet = self.get_object()
        amount = Money(request.data.get('amount'), request.data.get('currency', "USD"))
        wallet.withdraw(amount)
        return Response(status=200)

