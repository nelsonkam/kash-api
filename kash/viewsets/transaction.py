from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet, ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from stellar_sdk.exceptions import BadRequestError

from kash.models import Wallet
from kash.serializers.transaction import QosicTransactionSerializer
from kash.utils import StellarHelpers


class QosicTransactionViewSet(ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = QosicTransactionSerializer
    lookup_field = 'reference'

    def get_queryset(self):
        return self.request.user.transaction_set.all()


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
