import logging

from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.utils.payment import rave_request
from kash.models import Transaction, VirtualCard
from kash.serializers.virtual_card import VirtualCardSerializer
from kash.utils import TransactionStatusEnum, Conversions

logger = logging.getLogger(__name__)


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
        if request.data.get('phone'):
            if request.data.get('amount'):
                amount = Money(request.data.get('amount'), "USD")
            elif request.data.get('initial_amount'):
                amount = Money(request.data.get('initial_amount'), "XOF")
            else:
                raise NotImplemented

            txn = card.purchase_momo(
                amount=amount,
                phone=request.data.get('phone'),
                gateway=request.data.get('gateway')
            )

            return Response({'txn_ref': txn.reference})
        else:
            amount = request.data.get('amount')
            card.purchase(
                amount=Money(amount, "XOF"),
                usd_amount=request.data.get('usd_amount')
            )
            return Response(status=200)

    @action(detail=True, methods=['post'])
    def fund(self, request, pk=None):
        card = self.get_object()
        if request.data.get('phone'):
            amount = Money(request.data.get('amount'), "USD")
            txn = card.fund_momo(
                amount=amount,
                phone=request.data.get('phone'),
                gateway=request.data.get('gateway')
            )
            return Response({'txn_ref': txn.reference})
        else:
            amount = request.data.get('amount')
            card.fund(
                amount=Money(amount, "XOF"),
                usd_amount=request.data.get('usd_amount')
            )
            return Response(status=200)

    @action(detail=True, methods=['post'])
    def convert(self, request, pk=None):
        currency = request.data.get('currency', 'USD')
        is_withdrawal = request.data.get('is_withdrawal', False)
        if currency.upper() == 'USD':
            amount = Money(request.data.get('amount'), "USD")
            amount = Conversions.get_xof_from_usd(amount, is_withdrawal=is_withdrawal)
        elif currency.upper() == 'XOF':
            amount = Money(request.data.get('amount'), 'XOF')
            amount = Conversions.get_usd_from_xof(amount)
        else:
            raise NotImplemented
        return Response({'amount': round(amount.amount), 'fees': 0})

    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        card = self.get_object()

        return Response(card.get_transactions())

    @action(detail=True, methods=['get'])
    def statement(self, request, pk=None):
        card = self.get_object()

        return Response(card.get_statement())

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
        raise Exception("Card withdrawal unavailable.")
        card.withdraw(
            Money(request.data.get('amount'), 'USD'),
            phone=request.data.get("phone"),
            gateway=request.data.get('gateway')
        )
        return Response(self.get_serializer(card).data)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], authentication_classes=[])
    def txn_callback(self, request):
        card_id = request.data.get("CardId")
        card = VirtualCard.objects.get(external_id=card_id)
        amount = request.data.get("Amount")
        merchant_name = request.data.get("MerchantName")
        description = request.data.get("Description")

        if request.data.get("Status").lower() == "failed":
            card.profile.push_notify("⚠️ Échec de transaction",
                                     f"Ta carte {card.nickname} n'a pas pu être débitée de ${amount} par {merchant_name}. Raison: {description}",
                                     card)
        else:
            if request.data.get("Type").lower() == "debit":
                card.profile.push_notify("Nouvelle transaction 💳",
                                         f"Ta carte {card.nickname} vient d'être débitée de ${amount} par {merchant_name}. {'Description: ' + description if description else ''}",
                                         card)
            else:
                card.profile.push_notify("Nouvelle transaction 💳",
                                         f"Ta carte {card.nickname} vient d'être créditée de ${amount} par {merchant_name}. {'Description: ' + description if description else ''}",
                                         card)
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
