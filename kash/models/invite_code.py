from django.db import models

from core.models.base import BaseModel, generate_ref_id
from kash.utils import generate_reference


def generate_code():
    return generate_ref_id(length=4)


class InviteCode(BaseModel):
    inviter = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE, related_name='invite_codes')
    code = models.CharField(max_length=10, default=generate_code, unique=True)
    used_at = models.DateTimeField(null=True)
    invited = models.OneToOneField('kash.UserProfile', on_delete=models.CASCADE, null=True, related_name='invite')
