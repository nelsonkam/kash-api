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

from kash.models import Transaction, Wallet, UserProfile
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

    @action(detail=True, methods=["GET"])
    def transactions(self, request: Request, external_id=None):
        wallet = self.get_object()
        cursor = request.query_params.get("cursor")
        transactions = StellarHelpers.horizon_server.payments().for_account(
            wallet.external_id
        ).include_failed(True).cursor(cursor).order(True).limit(50).call()
        transactions = transactions.get("_embedded").get("records")

        source_accts = Wallet.objects.filter(
            external_id__in=[txn.get('to') for txn in transactions] + [txn.get('from') for txn in transactions]
        ).distinct('external_id').values_list('profile__kashtag', 'external_id')
        source_accts = list(source_accts)

        def get_kashtag(txn):
            source_account = txn.get('to') if txn.get('from') == wallet.external_id else txn.get('from')
            if source_account == StellarHelpers.master_keypair.public_key:
                return "Kash"
            else:
                kashtags = [kashtag for kashtag, external_id in source_accts if external_id == source_account]
                return f"${kashtags[0]}" if len(kashtags) > 0 else "Anonyme"

        def get_memo(txn):
            data = StellarHelpers.horizon_server.transactions().transaction(txn.get('transaction_hash')).call()
            if data.get('memo_type') == 'text':
                return data.get('memo')
            return None

        return Response([{
            'id': txn.get('id'),
            'cursor': txn.get('paging_token'),
            'successful': txn.get('transaction_successful'),
            'created_at': txn.get('created_at'),
            'type': 'debit' if txn.get('from') == wallet.external_id else 'credit',
            'amount': txn.get('amount'),
            'source': get_kashtag(txn),
            'memo': get_memo(txn)
        } for txn in transactions if txn.get('type') == 'payment'])

    @action(detail=True, methods=["POST"])
    def deposit(self, request, external_id=None):
        wallet = self.get_object()
        amount = Decimal(request.data.get("amount"))
        if request.data.get("currency").upper() == "XOF":
            xof_amount = amount
            usd_amount = Decimal(round(amount / Conversions.get_xof_usd_deposit_rate(), 2))
        elif request.data.get("currency").upper() == "USD":
            xof_amount = amount * Conversions.get_xof_usd_deposit_rate()
            usd_amount = amount
        else:
            raise NotImplemented
        usd_amount = Money(usd_amount, request.data.get('currency'))
        xof_amount = Money(xof_amount, request.data.get('currency'))
        phone = request.data.get('phone')
        gateway = request.data.get('gateway')

        if Transaction.objects.filter(
                initiator=request.user,
                status=TransactionStatusEnum.pending,
                transaction_type=TransactionType.payment).exists():
            raise Throttled

        wallet.initiate_deposit(usd_amount)
        txn = Transaction.objects.request(**{
            'obj': wallet,
            'name': wallet.profile.name,
            'amount': xof_amount,
            'phone': phone,
            'gateway': gateway,
            'initiator': wallet.profile.user
        })
        return Response({'txn_ref': txn.reference})

    @action(detail=True, methods=["POST"])
    def withdraw(self, request, external_id=None):
        wallet = self.get_object()
        amount = Money(request.data.get('amount'), request.data.get('currency', "USD"))
        wallet.withdraw(amount)
        return Response(status=200)

    @action(detail=True, methods=["POST"])
    def transfer(self, request, external_id=None):
        wallet = self.get_object()
        tags = request.data.get("recipient_tags")
        profiles = UserProfile.objects.filter(kashtag__in=tags)
        nowallet_profiles = profiles.filter(wallet__isnull=True)
        for profile in nowallet_profiles:
            Wallet.objects.create(profile=profile)
        wallets = Wallet.objects.filter(profile__kashtag__in=tags)
        wallet.bulk_transfer(wallets, Money(request.data.get("amount"), "USD"), request.data.get("note"))
        return Response(status=200)

