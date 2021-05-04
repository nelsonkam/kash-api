from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.serializers import UserSerializer
from kash.models import UserProfile
from kash.serializers.invite_code import InviteCodeSerializer
from kash.serializers.payout_method import MomoAccountSerializer


class ProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    name = serializers.CharField()
    payout_methods = serializers.SerializerMethodField()
    momo_accounts = serializers.SerializerMethodField()
    invite = InviteCodeSerializer(read_only=True)

    def get_payout_methods(self, obj):
        serializer = MomoAccountSerializer(obj.momo_accounts.all(), many=True)
        if len(serializer.data) == 0:
            return None
        return serializer.data

    def get_momo_accounts(self, obj):
        serializer = MomoAccountSerializer(obj.momo_accounts.all(), many=True)
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

    def update(self, instance, validated_data):
        name = validated_data.pop('name', None)
        instance = super(ProfileSerializer, self).update(instance, validated_data)
        instance.user.name = name
        instance.user.username = instance.kashtag
        instance.user.save()
        return instance

    class Meta:
        model = UserProfile
        fields = ['kashtag', 'txn_summary', 'limits', 'avatar_url', 'device_ids', 'user', 'name', 'payout_methods',
                  'momo_accounts', 'invite', 'kyc_level', 'phone_number']


class LimitedProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['kashtag', 'avatar_url', 'name']
