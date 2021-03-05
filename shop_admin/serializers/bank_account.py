from rest_framework.serializers import ModelSerializer

from core.models import BankAccount


class BankAccountSerializer(ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['external_id', 'account_number', "account_bank", 'service', 'created_at', 'updated_at']
