from rest_framework import serializers
from rest_framework.exceptions import Throttled
from rest_framework.fields import SerializerMethodField

from kash.models import UserProfile, KashRequest, KashRequestResponse, Notification
from kash.serializers.profile import ProfileSerializer, LimitedProfileSerializer


class KashRequestResponseSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(read_only=True, slug_field='kashtag')
    class Meta:
        model = KashRequestResponse
        fields = ['sender', 'accepted']


class KashRequestSerializer(serializers.ModelSerializer):
    initiator = LimitedProfileSerializer(read_only=True)
    recipient_tags = serializers.ListSerializer(child=serializers.CharField(), write_only=True)
    responses = KashRequestResponseSerializer(many=True, read_only=True)
    formatted = SerializerMethodField(read_only=True)

    def get_formatted(self, obj):
        amount = obj.amount.amount
        sender_name = f"${obj.initiator.kashtag}"
        return {
            'title': "Besoin de kash 💰",
            'description': f"{sender_name} a besoin de {amount} FCFA pour \"{obj.note}\""
        }

    def create(self, validated_data):
        tags = validated_data.pop('recipient_tags')
        initiator = validated_data.get('initiator')
        if len(tags) > 5:
            notif = Notification.objects.create(
                title="Fais doucement oh 😩",
                description="Essaie de demander du kash à 3 personnes max. à la fois.",
                content_object=initiator,
                profile=initiator
            )
            notif.send()
            raise Throttled

        recipients = UserProfile.objects.filter(kashtag__in=tags)
        kash_request = KashRequest.objects.create(**validated_data)
        kash_request.recipients.set(recipients)
        kash_request.save()
        kash_request.notify_recipients()
        return kash_request


    class Meta:
        model = KashRequest
        fields = ['id', 'recipient_tags', 'initiator', 'note', 'amount',
                  'amount_currency', 'responses', 'formatted']
