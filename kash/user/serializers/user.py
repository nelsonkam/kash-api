from kash.abstract.serializers import KashObjectSerializer

from kash.user.models import User


class UserSerializer(KashObjectSerializer):
    class Meta:
        model = User
        fields = KashObjectSerializer.Meta.fields + (
            "first_name",
            "email",
            "phone_number",
            "name",
        )
