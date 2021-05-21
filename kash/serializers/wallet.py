from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from core.utils import money_to_dict
from kash.models import Wallet


class WalletSerializer(ModelSerializer):
    xof_amount = serializers.SerializerMethodField()

    def get_xof_amount(self, obj):
        return money_to_dict(obj.xof_amount)

    class Meta:
        model = Wallet
        fields = ["external_id", "xof_amount", "balance"]



