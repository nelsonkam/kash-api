from rest_framework import serializers

from core.utils import money_to_dict
from kash.models import KashTransaction, UserProfile
from kash.serializers.profile import ProfileSerializer


class KashTransactionSerializer(serializers.ModelSerializer):
    recipients = ProfileSerializer(many=True, read_only=True)
    initiator = ProfileSerializer(read_only=True)
    recipient_tags = serializers.ListSerializer(child=serializers.CharField(), write_only=True)
    total = serializers.SerializerMethodField()
    fees = serializers.SerializerMethodField()

    def get_total(self, obj):
        return money_to_dict(obj.total)

    def get_fees(self, obj):
        return money_to_dict(obj.fees)

    def create(self, validated_data):
        tags = validated_data.pop('recipient_tags')
        recipients = UserProfile.objects.filter(kashtag__in=tags)
        kash_txn = KashTransaction.objects.create(**validated_data)
        kash_txn.recipients.set(recipients)
        kash_txn.save()
        return kash_txn

    class Meta:
        model = KashTransaction
        fields = ['id', 'recipients', 'recipient_tags', 'initiator', 'note', 'group_mode', 'is_incognito', 'amount',
                  'amount_currency', 'total', 'fees']
