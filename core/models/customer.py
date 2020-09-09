from django.db import models

from core.models.base import BaseModel


class Customer(BaseModel):
    name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'customers'
