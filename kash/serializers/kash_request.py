from rest_framework import serializers
from rest_framework.exceptions import Throttled
from rest_framework.fields import SerializerMethodField

from core.utils import money_to_dict
from kash.models import UserProfile, KashRequest, KashRequestResponse, Notification
from kash.serializers.profile import ProfileSerializer, LimitedProfileSerializer

class KashRequestSerializer(serializers.ModelSerializer):
    recipient = LimitedProfileSerializer(read_only=True)
    initiator = LimitedProfileSerializer(read_only=True)
    recipient_tag = serializers.CharField(write_only=True)
    formatted = SerializerMethodField(read_only=True)
    responses = SerializerMethodField(read_only=True)

    # Depreacted. v1 Legacy
    def get_responses(self, obj):
        if obj.accepted_at or obj.rejected_at:
            return [{'sender': obj.recipient.kashtag, 'accepted': bool(obj.accepted_at)}]
        return []

    def get_formatted(self, obj):
        amount = obj.amount.amount
        sender_name = f"${obj.initiator.kashtag}"
        return {
            'title': "Besoin de kash 💰",
            'description': f"{sender_name} a besoin de {amount} FCFA pour \"{obj.note}\""
        }

    def create(self, validated_data):
        tag = validated_data.pop('recipient_tag')
        recipient = UserProfile.objects.get(kashtag=tag)
        kash_request = KashRequest.objects.create(**validated_data, recipient=recipient)
        kash_request.notify_recipient()
        return kash_request

    class Meta:
        model = KashRequest
        fields = ['id', 'recipient', 'recipient_tag', 'initiator', 'note', 'amount',
                  'amount_currency', 'responses', 'formatted', 'created_at', 'accepted_at',
                  'rejected_at']
