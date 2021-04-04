from rest_framework.serializers import BaseSerializer, ModelSerializer

from kash.models import PayoutMethod


class PayoutMethodSerializer(ModelSerializer):

    class Meta:
        model = PayoutMethod
        fields = ['phone', 'gateway', 'id']
