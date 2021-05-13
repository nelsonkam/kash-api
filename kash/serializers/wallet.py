from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from core.utils import money_to_dict
from kash.models import Wallet, WalletTransaction


class WalletSerializer(ModelSerializer):
    xof_amount = serializers.SerializerMethodField()

    def get_xof_amount(self, obj):
        return money_to_dict(obj.xof_amount)

    class Meta:
        model = Wallet
        fields = ["balance", "balance_currency", "xof_amount"]


class WalletTransactionSerializer(ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = ["amount",
                  "amount_currency",
                  "running_balance",
                  "running_balance_currency",
                  "merchant", "narration",
                  "timestamp", "is_anonymous"]
