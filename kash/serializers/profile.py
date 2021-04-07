from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.serializers import UserSerializer
from kash.models import UserProfile
from kash.serializers.invite_code import InviteCodeSerializer
from kash.serializers.payout_method import PayoutMethodSerializer


class ProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    name = serializers.CharField()
    payout_methods = serializers.SerializerMethodField()
    invite = InviteCodeSerializer(read_only=True)

    def get_payout_methods(self, obj):
        serializer = PayoutMethodSerializer(obj.payout_methods.all(), many=True)
        if len(serializer.data) == 0:
            return None
        return serializer.data

    def create(self, validated_data):
        name = validated_data.pop('name')
        profile = UserProfile.objects.create(**validated_data)
        profile.save()
        profile.user.name = name
        profile.user.save()
        return profile

    class Meta:
        model = UserProfile
        fields = ['kashtag', 'avatar_url', 'device_ids', 'user', 'name', 'payout_methods', 'invite']
