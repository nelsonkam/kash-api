import secrets

from django.db import models
from django.utils.text import slugify

from core.models.base import BaseModel


class Product(BaseModel):
    name = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    currency_iso = models.CharField(max_length=10)
    shop = models.ForeignKey('core.Shop', models.CASCADE)
    category = models.ForeignKey('core.Category', models.SET_NULL, blank=True, null=True)
    slug = models.CharField(unique=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + secrets.token_urlsafe(2)
        super().save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'products'
