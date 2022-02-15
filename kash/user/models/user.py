from django.contrib.auth.models import AbstractUser
from django.db import models

from kash.abstract.models import BaseModel


class User(AbstractUser, BaseModel):
    username = models.CharField(unique=True, max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255)
    avatar_url = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "users"
