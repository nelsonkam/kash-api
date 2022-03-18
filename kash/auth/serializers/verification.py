import logging

import phonenumbers
from phonenumbers import NumberParseException
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from kash.auth.models import VerificationMethod
from kash.xlib.constants import PHONE_PREFIX_BLACKLIST
from kash.xlib.enums import VerificationMethodType

logger = logging.getLogger(__name__)


class LinkVerificationMethodSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    value = serializers.CharField(required=True)

    def validate_type(self, verification_method_type):
        if verification_method_type not in VerificationMethodType.values:
            raise ValidationError(
                "Invalid verification method type",
                code="invalid_verification_method_type",
            )
        return verification_method_type

    def validate(self, attrs):
        verification_method_type = attrs.get("type")
        if VerificationMethod.objects.filter(
            type=verification_method_type, value=attrs.get("value"), is_verified=True
        ).exists():
            raise ValidationError(
                {"value": "Verification method is already associated to an account"},
                code="unique_verification_method",
            )
        if verification_method_type == VerificationMethodType.phone:
            phone_number = attrs.get("value")

            try:
                formatted = phonenumbers.parse(phone_number, None)
            except NumberParseException:
                raise ValidationError({"value": "Invalid phone number"})
            if not phonenumbers.is_valid_number(formatted):
                raise ValidationError({"value": "Invalid phone number"})

            for prefix in PHONE_PREFIX_BLACKLIST:
                if phone_number.startswith(prefix):
                    raise ValidationError(
                        {"value": "Phone number blacklisted"},
                        code="phone_number_blacklisted",
                    )
        return attrs


class VerifyVerificationMethodSerializer(serializers.Serializer):
    session_token = serializers.CharField(required=True)
    security_code = serializers.CharField(required=True)


class VerificationMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationMethod
        fields = ["type", "value", "is_verified"]
