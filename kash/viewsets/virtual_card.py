import logging

from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money
from moneyed import Currency
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.utils.payment import rave_request
from kash.models import Transaction, VirtualCard, WithdrawalHistory
from kash.serializers.virtual_card import VirtualCardSerializer, WithdrawalHistorySerializer
from kash.utils import TransactionStatusEnum, Conversions, TransactionStatus

logger = logging.getLogger(__name__)


class VirtualCardViewSet(ModelViewSet):
    serializer_class = VirtualCardSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.profile.virtualcard_set.all().order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response([{**data, 'card_details': {
            'card_type': "visa",
            'amount': "Active",
            'currency': "",
            'masked_pan': f"****{data.get('last_4')}",
            'card_pan': '',
            'expiration': ''
        } if data.get("external_id") else None} for data in serializer.data])

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({**serializer.data, 'card_details': instance.card_details})

    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        card = self.get_object()
        if request.data.get('amount'):
            amount = Money(request.data.get('amount'), "USD")
        elif request.data.get('initial_amount'):
            amount = Money(request.data.get('initial_amount'), "XOF")
        else:
            card.profile.push_notify("Création de ta carte ⚠️",
                                     "Réessaies en spécifiant un montant à recharger "
                                     "à la création de ta carte ($5 minimum)",
                                     card)
            raise NotImplementedError()

        txn = card.purchase_momo(
            amount=amount,
            phone=request.data.get('phone'),
            gateway=request.data.get('gateway')
        )

        return Response({'txn_ref': txn.reference})

    @action(detail=True, methods=['post'])
    def fund(self, request, pk=None):
        card = self.get_object()
        amount = Money(request.data.get('amount'), "USD")
        txn = card.fund_momo(
            amount=amount,
            phone=request.data.get('phone'),
            gateway=request.data.get('gateway')
        )
        return Response({'txn_ref': txn.reference})

    @action(detail=True, methods=['post'])
    def convert(self, request, pk=None):
        currency = request.data.get('currency', 'USD')
        is_withdrawal = request.data.get('is_withdrawal', False)
        if currency.upper() == 'USD':
            amount = Money(request.data.get('amount'), "USD")
            amount = Conversions.get_xof_from_usd(
                amount, is_withdrawal=is_withdrawal)
        elif currency.upper() == 'XOF':
            amount = Money(request.data.get('amount'), 'XOF')
            amount = Conversions.get_usd_from_xof(amount)
        else:
            raise NotImplemented
        return Response({'amount': round(amount.amount), 'fees': 0})

    @action(detail=True, methods=['post'], url_path="txn/preview")
    def txn_preview(self, request, pk=None):
        card = self.get_object()
        operation = request.data.get("operation")
        currency = request.data.get('currency', 'USD')
        is_withdrawal = request.data.get('is_withdrawal', False)
        if currency.upper() == 'USD':
            amount = Money(request.data.get('amount'), "USD")
            amount = Conversions.get_xof_from_usd(
                amount, is_withdrawal=is_withdrawal)
        elif currency.upper() == 'XOF':
            amount = Money(request.data.get('amount'), 'XOF')
            amount = Conversions.get_usd_from_xof(amount)
        else:
            raise NotImplemented
        amount = round(amount.amount)
        discount = min(card.profile.promo_balance,
                       1000) if not is_withdrawal else 0

        if operation == 'purchase':
            amount += card.issuance_cost.amount

        return Response({
            'amount': {
                'amount': amount,
                'currency': "XOF"
            },
            'discount': {
                'amount': discount,
                'currency': "XOF"
            },
            'total': {
                'amount': max(amount - discount, 0),
                'currency': "XOF"
            },
            'fees': {'amount': 0, 'currency': "XOF"}
        })

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

        if description and description.lower() == "otp":
            card.profile.push_notify("Code OTP", f"Le code OTP pour votre transaction est: {request.data.get('Otp')}", card)
        else:
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

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser])
    def search(self, request):
        search = request.query_params.get("s")
        cards = VirtualCard.objects.filter(last_4=search)
        return Response(data=self.get_serializer(cards, many=True).data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsAdminUser], url_path="history/withdrawal")
    def withdrawal_history(self, request, pk=None):
        card = self.get_object()
        history = card.withdrawalhistory_set.all()
        return Response(data=WithdrawalHistorySerializer(history, many=True).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser],
            url_path="withdrawal/credit")
    def credit_withdrawal(self, request, pk=None):
        card = self.get_object()
        withdrawal = get_object_or_404(card.withdrawalhistory_set.all(), pk=request.data.get("withdrawal_id"))
        if withdrawal.status == WithdrawalHistory.Status.withdrawn:
            card.provider.fund(card, withdrawal.amount)
            withdrawal.status = WithdrawalHistory.Status.failed
            withdrawal.save()
        return Response(data=WithdrawalHistorySerializer(withdrawal).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser],
            url_path="withdrawal/payout")
    def payout_withdrawal(self, request, pk=None):
        card = self.get_object()
        withdrawal = get_object_or_404(card.withdrawalhistory_set.all(), pk=request.data.get("withdrawal_id"))
        withdrawal.payout()
        return Response(data=WithdrawalHistorySerializer(withdrawal).data)

    # Deprecated: Only available for legacy reasons
    @action(detail=True, methods=['post'], url_path='purchase/confirm')
    def purchase_confirm(self, request, pk=None):
        card = self.get_object()
        reference = request.data.get('txn_ref')
        txn = Transaction.objects.get(reference=reference)
        if txn.content_object == card and txn.status == TransactionStatus.success:
            return Response(status=201)
        return Response(status=400)

    # Deprecated: Only available for legacy reasons, use /convert/ instead
    @action(detail=True, methods=['post'])
    def funding_details(self, request, pk=None):
        return self.convert(request, pk=pk)
