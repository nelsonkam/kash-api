from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from kash.models import Notification, KashRequest, KashTransaction
from kash.serializers.kash_request import KashRequestSerializer
from kash.serializers.kash_transaction import KashTransactionSerializer


class NotificationObjectSerializer(serializers.RelatedField):

    def to_representation(self, value):
        instance_type = None
        if isinstance(value, KashRequest):
            serializer = KashRequestSerializer(value)
            instance_type = "request"
        elif isinstance(value, KashTransaction):
            serializer = KashTransactionSerializer(value)
            instance_type = "transaction"
        else:
            raise Exception('Unexpected type of notification object')

        return {**serializer.data, 'type': instance_type}


class NotificationSerializer(ModelSerializer):
    content_object = NotificationObjectSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'title', 'description', 'created_at', 'content_object']
