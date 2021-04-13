from rest_framework import serializers

from core.utils import money_to_dict
from kash.models import SendKash, UserProfile
from kash.serializers.profile import ProfileSerializer, LimitedProfileSerializer


class SendKashSerializer(serializers.ModelSerializer):
    initiator = LimitedProfileSerializer(read_only=True)
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
        kash_txn = SendKash.objects.create(**validated_data)
        kash_txn.recipients.set(recipients)
        kash_txn.save()
        return kash_txn

    class Meta:
        model = SendKash
        fields = ['id', 'recipient_tags', 'initiator', 'note', 'group_mode', 'is_incognito', 'amount',
                  'amount_currency', 'total', 'fees']
