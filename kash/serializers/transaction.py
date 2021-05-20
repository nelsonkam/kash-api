from rest_framework.serializers import ModelSerializer

from kash.models import Transaction


class QosicTransactionSerializer(ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['reference', 'created', 'status', 'amount', 'amount_currency']
