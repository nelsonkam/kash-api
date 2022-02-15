from rest_framework.serializers import ModelSerializer

from kash.payout.models import MomoAccount


class MomoAccountSerializer(ModelSerializer):
    class Meta:
        model = MomoAccount
        fields = ["phone", "gateway", "id"]
