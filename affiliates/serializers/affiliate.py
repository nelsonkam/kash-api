from rest_framework import serializers

from core.models import AffiliateAgent
from core.serializers import UserSerializer
from core.serializers.base import BaseModelSerializer


class AffiliateAgentSerializer(BaseModelSerializer):
    name = serializers.CharField(write_only=True)
    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        user = validated_data.pop("user")
        user.name = validated_data.pop("name")
        user.save()
        if hasattr(user, 'affiliate'):
            return user.affiliate
        return AffiliateAgent.objects.create(user=user, **validated_data)

    class Meta:
        model = AffiliateAgent
        fields = ["id", "user", "code", "name", "momo_number", "balance", "order_count"]
        depth = 1
