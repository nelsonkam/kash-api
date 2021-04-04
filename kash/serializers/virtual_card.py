from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from core.utils import money_to_dict
from kash.models import VirtualCard


class VirtualCardSerializer(ModelSerializer):
    issuance_cost = SerializerMethodField()

    def get_issuance_cost(self, obj):
        return money_to_dict(obj.issuance_cost)

    class Meta:
        model = VirtualCard
        fields = ['nickname', 'card_details', 'id', 'issuance_cost']
