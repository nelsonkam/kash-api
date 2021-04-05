from rest_framework import serializers

from kash.models import UserProfile, KashRequest, KashRequestResponse
from kash.serializers.profile import ProfileSerializer

class KashRequestResponseSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(read_only=True, slug_field='kashtag')
    class Meta:
        model = KashRequestResponse
        fields = ['sender', 'accepted']


class KashRequestSerializer(serializers.ModelSerializer):
    recipients = ProfileSerializer(many=True, read_only=True)
    initiator = ProfileSerializer(read_only=True)
    recipient_tags = serializers.ListSerializer(child=serializers.CharField(), write_only=True)
    responses = KashRequestResponseSerializer(many=True, read_only=True)

    def create(self, validated_data):
        tags = validated_data.pop('recipient_tags')
        recipients = UserProfile.objects.filter(kashtag__in=tags)
        kash_request = KashRequest.objects.create(**validated_data)
        kash_request.recipients.set(recipients)
        kash_request.save()
        kash_request.notify_recipients()
        return kash_request

    class Meta:
        model = KashRequest
        fields = ['id', 'recipients', 'recipient_tags', 'initiator', 'note', 'amount',
                  'amount_currency', 'responses']
