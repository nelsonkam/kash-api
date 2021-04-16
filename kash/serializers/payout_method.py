from rest_framework.serializers import BaseSerializer, ModelSerializer

from kash.models import MomoAccount


class MomoAccountSerializer(ModelSerializer):

    class Meta:
        model = MomoAccount
        fields = ['phone', 'gateway', 'id']
