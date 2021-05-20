from rest_framework import serializers

from core.models import User
from core.serializers.base import BaseModelSerializer


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "name",
            "email",
            "phone_number",
        ]
        depth = 1
