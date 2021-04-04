from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.serializers import UserSerializer
from kash.models import UserProfile
from kash.serializers.payout_method import PayoutMethodSerializer


class ProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    name = serializers.CharField()
    payout_methods = PayoutMethodSerializer(many=True, read_only=True)

    def create(self, validated_data):
        name = validated_data.pop('name')
        profile = UserProfile.objects.create(**validated_data)
        profile.save()
        profile.user.name = name
        profile.user.save()
        return profile

    class Meta:
        model = UserProfile
        fields = ['kashtag', 'device_ids', 'user', 'name', 'payout_methods']
