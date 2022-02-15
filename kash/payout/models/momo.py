from django.db import models

from kash.abstract.models import BaseModel
from kash.xlib.utils.utils import GatewayEnum


class MomoAccount(BaseModel):
    profile = models.ForeignKey(
        "kash.UserProfile", on_delete=models.CASCADE, related_name="momo_accounts"
    )
    gateway = models.CharField(max_length=20, choices=GatewayEnum.items())
    phone = models.CharField(max_length=45)
