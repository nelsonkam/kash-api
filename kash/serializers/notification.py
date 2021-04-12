from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from kash.models import Notification, KashRequest, KashTransaction, VirtualCard, UserProfile
from kash.serializers.kash_request import KashRequestSerializer
from kash.serializers.kash_transaction import KashTransactionSerializer
from kash.serializers.profile import ProfileSerializer
from kash.serializers.virtual_card import VirtualCardSerializer


class NotificationObjectSerializer(serializers.RelatedField):

    def to_representation(self, value):
        instance_type = None
        if isinstance(value, KashRequest):
            serializer = KashRequestSerializer(value)
            instance_type = "request"
        elif isinstance(value, KashTransaction):
            serializer = KashTransactionSerializer(value)
            instance_type = "transaction"
        elif isinstance(value, VirtualCard):
            serializer = VirtualCardSerializer(value)
            instance_type = "virtual-card"
        elif isinstance(value, UserProfile):
            serializer = ProfileSerializer(value)
            instance_type = "profile-throttle"
        else:
            raise Exception('Unexpected type of notification object')

        return {**serializer.data, 'type': instance_type}


class NotificationSerializer(ModelSerializer):
    content_object = NotificationObjectSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'title', 'description', 'created_at', 'content_object']
