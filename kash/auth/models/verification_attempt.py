import random
from datetime import timedelta

import jwt
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.crypto import get_random_string

from kash.abstract.models import BaseModel
from django.db import models

from kash.xlib.enums import VerificationMethodType
from kash.xlib.utils.messaging import send_sms, send_email


def generate_security_code():
    if not settings.IS_PROD:
        return "123456"
    return get_random_string(6, allowed_chars="0123456789")


def generate_session_token(verification_method_id):
    """
    Returns a unique session_token for
    identifying a particular device in subsequent calls.
    """
    data = {"verification_method_id": verification_method_id, "nonce": random.random()}
    return jwt.encode(data, settings.SECRET_KEY).decode()


class VerificationAttemptManager(models.Manager):
    def create(self, verification_method):
        attempt = self.model(
            verification_method=verification_method,
            session_token=generate_session_token(verification_method.pk),
            type=verification_method.type,
            value=verification_method.value,
        )
        attempt.save()
        return attempt

    def verify_attempt(self, session_token, security_code):
        attempt = self.filter(
            session_token=session_token, security_code=security_code
        ).first()
        if not attempt:
            return None, "invalid_security_code"

        if (timezone.now() - attempt.created_at) > timedelta(minutes=30):
            return None, "expired_security_code"

        if attempt.is_verified:
            return None, "used_security_code"

        attempt.set_verified(is_verified=True)
        return attempt, None


class VerificationAttempt(BaseModel):
    security_code = models.CharField(max_length=120, default=generate_security_code)
    session_token = models.CharField(max_length=500)
    is_verified = models.BooleanField(default=False)
    value = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=VerificationMethodType.choices)
    verification_method = models.ForeignKey(
        "kash_auth.VerificationMethod",
        on_delete=models.CASCADE,
        related_name="verification_attempt",
    )

    objects = VerificationAttemptManager()

    def send_security_code(self):
        if self.type == VerificationMethodType.phone:
            send_sms(
                self.value,
                f"Votre code de verification pour Kash est: {self.security_code}",
            )
        elif self.type == VerificationMethodType.email:
            send_email(
                email_address=self.value,
                subject="Votre code de vérification",
                template="auth/verification_code.html",
                context={"code": self.security_code},
            )

    def set_verified(self, is_verified):
        self.is_verified = is_verified
        self.save(update_fields=["is_verified"])
        if not self.verification_method.is_verified and is_verified:
            self.verification_method.is_verified = is_verified
            self.verification_method.save(update_fields=["is_verified"])
