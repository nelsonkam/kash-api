from django.db import models

from core.models.base import BaseModel
from kash.utils import GatewayEnum


class PayoutMethod(BaseModel):
    profile = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE, related_name='payout_methods')
    gateway = models.CharField(max_length=20, choices=GatewayEnum.items())
    phone = models.CharField(max_length=45)
