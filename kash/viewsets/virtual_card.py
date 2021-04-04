from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.models import Transaction
from kash.serializers.virtual_card import VirtualCardSerializer
from kash.utils import TransactionStatusEnum


class VirtualCardViewSet(ModelViewSet):
    serializer_class = VirtualCardSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.profile.virtualcard_set.all()

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        card = self.get_object()
        txn = card.purchase(
            initial_amount=request.data.get('initial_amount'),
            phone=request.data.get('phone'),
            gateway=request.data.get('gateway')
        )
        return Response({'txn_ref': txn.reference})

    @action(detail=True, methods=['post'], url_path='purchase/confirm')
    def purchase_confirm(self, request, pk=None):
        card = self.get_object()
        reference = request.data.get('txn_ref')
        txn = Transaction.objects.get(reference=reference)
        if txn.content_object == card and txn.status == TransactionStatusEnum.success.value:
            card.create_external(amount=txn.amount - card.issuance_cost)
            return Response(status=201)

        return Response(status=400)

    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        card = self.get_object()

        return Response(card.get_transactions())

