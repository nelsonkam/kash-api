from django.db import models

from kash.abstract.models import BaseModel
from kash.xlib.enums import VerificationMethodType


class VerificationMethod(BaseModel):
    type = models.CharField(max_length=20, choices=VerificationMethodType.choices)
    value = models.CharField(max_length=255)
    is_verified = models.BooleanField()
    user = models.ForeignKey(
        "kash_user.User",
        on_delete=models.CASCADE,
        related_name="verification_methods",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "value", "is_verified"],
                name="unique_verified_verificationmethod",
            )
        ]
