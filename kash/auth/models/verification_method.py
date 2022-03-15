from django.db import models

from kash.abstract.models import BaseModel


class VerificationMethod(BaseModel):
    class VerificationMethodType(models.TextChoices):
        phone = "Phone"
        email = "Email"

    type = models.CharField(max_length=20, choices=VerificationMethodType.choices)
    value = models.CharField(max_length=255, unique=True)
    is_verified = models.BooleanField()
    profile = models.ForeignKey("kash_user.UserProfile", on_delete=models.CASCADE, related_name="verification_methods")
