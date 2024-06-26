from rest_framework.serializers import ModelSerializer

from kash.transaction.models import Transaction


class QosicTransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "reference",
            "created",
            "status",
            "amount",
            "amount_currency",
            "name",
            "phone",
            "gateway",
            "transaction_type",
        ]
