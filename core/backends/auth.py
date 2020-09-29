from django.contrib.auth.backends import BaseBackend
from phone_verify.serializers import SMSVerificationSerializer

from core.models import User


class SMSAuthBackend(BaseBackend):
    def authenticate(
        self,
        request,
        phone_number=None,
        security_code=None,
        session_token=None,
        **kwargs
    ):
        serializer = SMSVerificationSerializer(
            data={
                "phone_number": phone_number,
                "security_code": security_code,
                "session_token": session_token,
            }
        )
        if serializer.is_valid():
            user, created = User.objects.get_or_create(
                username=phone_number, defaults=dict(phone_number=phone_number)
            )
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
