from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from kash.models import Notification, KashRequest, SendKash, VirtualCard, UserProfile
from kash.serializers.kash_request import KashRequestSerializer
from kash.serializers.send_kash import SendKashSerializer
from kash.serializers.profile import ProfileSerializer, LimitedProfileSerializer
from kash.serializers.virtual_card import VirtualCardSerializer


class NotificationObjectSerializer(serializers.RelatedField):

    def to_representation(self, value):
        instance_type = None
        if isinstance(value, KashRequest):
            serializer = KashRequestSerializer(value)
            instance_type = "request"
        elif isinstance(value, SendKash):
            serializer = SendKashSerializer(value)
            instance_type = "transaction"
        elif isinstance(value, VirtualCard):
            serializer = VirtualCardSerializer(value)
            instance_type = "virtual-card"
        elif isinstance(value, UserProfile):
            serializer = LimitedProfileSerializer(value)
            instance_type = "profile-throttle"
        else:
            return {type: "unknown", 'responses': []}

        return {**serializer.data, 'type': instance_type}


class NotificationSerializer(ModelSerializer):
    content_object = SerializerMethodField(read_only=True)

    def get_content_object(self, obj):
        value = obj.content_object

        if isinstance(value, KashRequest):
            serializer = KashRequestSerializer(value)
            instance_type = "request"
        elif isinstance(value, SendKash):
            serializer = SendKashSerializer(value)
            instance_type = "transaction"
        elif isinstance(value, VirtualCard):
            serializer = VirtualCardSerializer(value)
            instance_type = "virtual-card"
        elif isinstance(value, UserProfile):
            serializer = LimitedProfileSerializer(value)
            instance_type = "profile-throttle"
        else:
            return {type: "unknown", 'responses': []}

        return {**serializer.data, 'type': instance_type}

    class Meta:
        model = Notification
        fields = ['id', 'title', 'description', 'created_at', 'content_object']
