import secrets
import string

from django.db import models


def generate_uid():
    return secrets.token_urlsafe(8)


def generate_affiliate_code():
    return generate_ref_id("A-", 4)


def generate_ref_id(prefix="", length=6):
    alphabet = string.ascii_uppercase + string.digits
    code = "".join(secrets.choice(alphabet) for i in range(length)).upper()
    return prefix + code


class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
