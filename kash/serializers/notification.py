from rest_framework.serializers import ModelSerializer

from kash.models import Notification


class NotificationSerializer(ModelSerializer):

    class Meta:
        model = Notification
        fields = ['id', 'title', 'description', 'created_at']
