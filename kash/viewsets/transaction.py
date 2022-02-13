from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet, ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from stellar_sdk.exceptions import BadRequestError

from kash.models import Wallet, Transaction, FundingHistory, WithdrawalHistory
from kash.serializers.transaction import QosicTransactionSerializer
from kash.serializers.virtual_card import FundingHistorySerializer, WithdrawalHistorySerializer
from kash.utils import StellarHelpers


class QosicTransactionViewSet(ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = QosicTransactionSerializer
    lookup_field = 'reference'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_object(self):
        if self.request.user and self.request.user.is_staff:
            queryset = self.filter_queryset(Transaction.objects.all())
        else:
            queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    def search(self, request):
        ref = request.query_params.get("ref")
        phone = request.query_params.get("phone")
        if ref:
            txns = Transaction.objects.filter(reference__icontains=ref)
        elif phone:
            txns = Transaction.objects.filter(phone__icontains=phone)
        else:
            raise ValidationError("Invalid query param")
        return Response(data=self.get_serializer(txns.order_by("-created"), many=True).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser], url_path="check-status")
    def check_status(self, request, reference=None):
        txn = get_object_or_404(Transaction, reference=reference)
        txn.check_status()
        return Response(data={'status': txn.status})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def retry(self, request, reference=None):
        txn = get_object_or_404(Transaction, reference=reference)
        txn.retry()
        return Response(data={'status': txn.status})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def refund(self, request, reference=None):
        txn = get_object_or_404(Transaction, reference=reference)
        txn.refund()
        return Response(data={'status': txn.status})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def fund(self, request, reference=None):
        history = get_object_or_404(FundingHistory, txn_ref=reference)
        history.fund()
        return Response(data={'status': history.status})

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser], url_path='funding/status')
    def funding_status(self, request, reference=None):
        history = get_object_or_404(FundingHistory, txn_ref=reference)
        serializer = FundingHistorySerializer(instance=history)
        return Response(data=serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser], url_path='history/status')
    def history_status(self, request, reference=None):
        history = get_object_or_404(WithdrawalHistory, txn_ref=reference)
        serializer = WithdrawalHistorySerializer(instance=history)
        return Response(data=serializer.data)


class StellarTransactionViewSet(ViewSet):
    def get_parent_object(self):
        if self.kwargs["wallet_external_id"] == "current":
            return self.request.user.profile.wallet
        return get_object_or_404(Wallet.objects.filter(profile=self.request.user.profile),
                                 external_id=self.kwargs["wallet_external_id"])

    def list(self, request, wallet_external_id=None):
        wallet = self.get_parent_object()
        cursor = request.query_params.get("cursor")
        payments = StellarHelpers.horizon_server.payments().for_account(
            wallet.external_id
        ).include_failed(True).order(True).limit(50).call()
        payments = payments.get("_embedded").get("records")

        return Response(StellarHelpers.format_payment_transactions(wallet, payments))

    def retrieve(self, request, pk=None, wallet_external_id=None):
        wallet = self.get_parent_object()
        try:
            response = StellarHelpers.horizon_server.operations().operation(pk).call()
        except BadRequestError:
            raise NotFound

        return Response(StellarHelpers.format_payment_transaction(wallet, response)[0])
