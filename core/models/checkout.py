from django.db import models

from core.models.base import BaseModel


class Checkout(BaseModel):
    customer = models.ForeignKey('core.Customer', models.CASCADE)
    cart = models.ForeignKey('core.Cart', models.CASCADE)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.TextField()
    uid = models.CharField(unique=True, max_length=40)
    shipping_option = models.JSONField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = True
        db_table = 'checkouts'
