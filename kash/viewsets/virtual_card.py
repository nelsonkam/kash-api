from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.utils.payment import rave_request
from kash.models import Transaction
from kash.serializers.virtual_card import VirtualCardSerializer
from kash.utils import TransactionStatusEnum


class VirtualCardViewSet(ModelViewSet):
    serializer_class = VirtualCardSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.profile.virtualcard_set.all().order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        card = self.get_object()
        if request.data.get('amount'):
            amount = Money(request.data.get('amount'), "USD")
        elif request.data.get('initial_amount'):
            amount = card.get_usd_from_xof(Money(request.data.get('initial_amount'), "XOF"))
        else:
            raise NotImplemented

        txn = card.purchase(
            amount=amount,
            phone=request.data.get('phone'),
            gateway=request.data.get('gateway')
        )

        return Response({'txn_ref': txn.reference})

    @action(detail=True, methods=['post'])
    def fund(self, request, pk=None):
        card = self.get_object()
        amount = Money(request.data.get('amount'), "USD")
        txn = card.fund(
            amount=amount,
            phone=request.data.get('phone'),
            gateway=request.data.get('gateway')
        )
        return Response({'txn_ref': txn.reference})

    @action(detail=True, methods=['post'])
    def convert(self, request, pk=None):
        card = self.get_object()
        amount = Money(request.data.get('amount'), "USD")
        amount = card.get_xof_from_usd(amount)
        return Response({'amount': round(amount.amount), 'fees': 0})

    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        card = self.get_object()

        return Response(card.get_transactions())

    @action(detail=True, methods=['post'])
    def freeze(self, request, pk=None):
        card = self.get_object()
        card.freeze()
        return Response(self.get_serializer(card).data)

    @action(detail=True, methods=['post'])
    def unfreeze(self, request, pk=None):
        card = self.get_object()
        card.unfreeze()
        return Response(self.get_serializer(card).data)

    @action(detail=True, methods=['post'])
    def terminate(self, request, pk=None):
        card = self.get_object()
        card.terminate()
        return Response(self.get_serializer(card).data)

    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk=None):
        card = self.get_object()
        card.withdraw(Money(request.data.get('amount'), 'USD'))
        return Response(self.get_serializer(card).data)

    @action(detail=False, methods=['post'], permission_classes=[])
    def txn_callback(self, request):
        print(request.data)
        return Response(status=200)

    # Deprecated: Only available for legacy reasons
    @action(detail=True, methods=['post'], url_path='purchase/confirm')
    def purchase_confirm(self, request, pk=None):
        card = self.get_object()
        reference = request.data.get('txn_ref')
        txn = Transaction.objects.get(reference=reference)
        if txn.content_object == card and txn.status == TransactionStatusEnum.success.value:
            return Response(status=201)
        return Response(status=400)

    # Deprecated: Only available for legacy reasons, use /convert/ instead
    @action(detail=True, methods=['post'])
    def funding_details(self, request, pk=None):
        return self.convert(request, pk=pk)


