from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import BaseSerializer

from kash.models.user_profile import KashtagValidator, UserProfile


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)
    confirm = serializers.CharField(write_only=True)
    kashtag = serializers.CharField(validators=[KashtagValidator], min_length=3, max_length=20)

    def validate_kashtag(self, value):
        if UserProfile.objects.filter(kashtag=value).exists():
            raise ValidationError('$kashtag already taken')

        return value

    def validate(self, data):
        if data.get('password') != data.get("confirm"):
            raise ValidationError("Passwords do not match.")
        return data