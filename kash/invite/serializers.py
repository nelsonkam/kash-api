from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from kash.invite.models import InviteCode


class InviteCodeSerializer(ModelSerializer):
    code = serializers.CharField(read_only=True)

    class Meta:
        model = InviteCode
        fields = ["id", "code"]
