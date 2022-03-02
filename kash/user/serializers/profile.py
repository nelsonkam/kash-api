from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from kash.user.models import UserProfile
from .user import UserSerializer


class ProfileSerializer(ModelSerializer):
    name = serializers.CharField()

    def update(self, instance, validated_data):
        name = validated_data.pop("name", None)
        instance = super(ProfileSerializer, self).update(instance, validated_data)
        # todo: how can we avoid tracking this twice (looks redundant)
        instance.user.name = name
        instance.user.username = instance.kashtag
        instance.user.save()
        return instance

    class Meta:
        model = UserProfile
        read_only_fields = ["referral_code", "promo_balance"]
        fields = [
            "kashtag",
            "avatar_url",
            "device_ids",
            "name",
            "phone_number",
            "referral_code",
            "promo_balance",
            "kyc_level"
        ]


class LimitedProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["kashtag", "avatar_url", "name"]
