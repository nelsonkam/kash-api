from django.contrib.auth import authenticate
from phone_verify.backends import get_sms_backend
from phone_verify.services import send_security_code_and_generate_session_token
from rest_framework.exceptions import (
    AuthenticationFailed,
    ValidationError,
    PermissionDenied,
)
from rest_framework_simplejwt.tokens import RefreshToken

from kash.auth.models import VerificationMethod, VerificationAttempt
from kash.user.models import User, UserProfile
from kash.user.serializers import UserSerializer
from kash.xlib.constants import PHONE_PREFIX_BLACKLIST
from kash.xlib.enums import VerificationMethodType


class AuthService:
    def register(self, username, name, password):
        user = User.objects.create_user(
            username=username,
            name=name,
            password=password,
        )
        UserProfile.objects.create(user=user, kashtag=username)

        return self.login(username, password)

    def login(self, request, username, password):
        user = authenticate(request, username=username, password=password)
        if not user:
            raise AuthenticationFailed("Invalid username/password")
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(instance=user).data,
        }

    def send_verification_code(self, user, data):
        method, _ = VerificationMethod.objects.get_or_create(
            type=data.get("type"),
            value=data.get("value"),
            user=user,
            defaults={
                "is_verified": False,
            },
        )
        attempt = VerificationAttempt.objects.create(
            method,
        )
        attempt.send_security_code()
        return attempt

    def verify_verification_attempt(self, security_code, session_token):
        return VerificationAttempt.objects.verify_attempt(
            security_code=security_code, session_token=session_token
        )

    # deprecated: only used in /profile/current/otp/phone/
    # (which is deprecated in favor of /auth/verification/link/)
    def send_phone_verification_code(self, user, phone_number: str):
        for prefix in PHONE_PREFIX_BLACKLIST:
            if phone_number.startswith(prefix):
                raise PermissionDenied
        method = VerificationMethod.objects.create(
            type=VerificationMethodType.phone,
            value=phone_number,
            is_verified=False,
            user=user,
        )
        attempt = VerificationAttempt.objects.create(
            method,
        )
        attempt.send_security_code()
        return attempt

    def link_phone_number(self, user, security_code, phone_number, session_token):

        if User.objects.filter(phone_number=phone_number).exists():
            raise PermissionDenied(
                "Vous ne pouvez pas ajouter ce numéro à votre compte."
            )

        backend = get_sms_backend(phone_number=phone_number)
        verification, error_code = backend.validate_security_code(
            security_code=security_code,
            phone_number=phone_number,
            session_token=session_token,
        )
        if verification:
            user.phone_number = phone_number
            user.save()
        else:
            message = "Une erreur est survenue. Veuillez réessayer."
            if error_code == backend.SECURITY_CODE_INVALID:
                message = "Code de vérification invalide. Veuillez réessayer"
            elif error_code == backend.SECURITY_CODE_EXPIRED:
                message = "Code de vérification expiré. Veuillez réessayer"
            elif error_code == backend.SESSION_TOKEN_INVALID:
                message = "Erreur de session. Veuillez réessayer"
            elif error_code == backend.SECURITY_CODE_VERIFIED:
                message = "Code de vérification déjà utilisé. Veuillez réessayer"
            user.profile.push_notify(
                "Erreur lors de la vérification.", message, obj=user
            )
            raise ValidationError({"message": message})
