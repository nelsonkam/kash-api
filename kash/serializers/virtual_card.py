from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, ListSerializer

from core.utils import money_to_dict
from kash.models import VirtualCard, FundingHistory


class VirtualCardSerializer(ModelSerializer):
    issuance_cost = SerializerMethodField()

    def get_issuance_cost(self, obj):
        return money_to_dict(obj.issuance_cost)

    class Meta:
        model = VirtualCard
        fields = ['nickname', 'category', 'is_active', 'last_4', 'card_type', 'external_id', 'id', 'issuance_cost']


class FundingHistorySerializer(ModelSerializer):
    card = VirtualCardSerializer(read_only=True)

    class Meta:
        model = FundingHistory
        fields = ['id', 'txn_ref', 'amount', 'status', 'retries', 'card']