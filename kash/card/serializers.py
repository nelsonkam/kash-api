from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from kash.xlib.utils import money_to_dict
from kash.card.models import VirtualCard, FundingHistory, WithdrawalHistory
from kash.transaction.models import Transaction
from kash.transaction.serializers import QosicTransactionSerializer


class VirtualCardSerializer(ModelSerializer):
    issuance_cost = SerializerMethodField()
    is_active = SerializerMethodField()

    def get_issuance_cost(self, obj):
        return money_to_dict(obj.issuance_cost)

    def get_is_active(self, obj):
        return obj.is_active or not obj.is_permablocked

    class Meta:
        model = VirtualCard
        fields = [
            "nickname",
            "category",
            "is_active",
            "last_4",
            "card_type",
            "external_id",
            "id",
            "issuance_cost",
        ]


class FundingHistorySerializer(ModelSerializer):
    card = VirtualCardSerializer(read_only=True)
    txn = SerializerMethodField()

    def get_txn(self, obj):
        if obj.txn_ref:
            txn = Transaction.objects.filter(reference=obj.txn_ref).first()
            if txn:
                return QosicTransactionSerializer(instance=txn).data
        return None

    class Meta:
        model = FundingHistory
        fields = ["id", "txn_ref", "amount", "status", "retries", "card", "txn"]


class WithdrawalHistorySerializer(ModelSerializer):
    card = VirtualCardSerializer(read_only=True)
    txn = SerializerMethodField()

    def get_txn(self, obj):
        if obj.txn_ref:
            txn = Transaction.objects.filter(reference=obj.txn_ref).first()
            if txn:
                return QosicTransactionSerializer(instance=txn).data
        return None

    class Meta:
        model = WithdrawalHistory
        fields = ["id", "txn_ref", "amount", "status", "card", "txn", "created_at"]
