import secrets

from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.text import slugify
from djmoney.models.fields import MoneyField

from core.models.base import BaseModel


class Product(BaseModel):
    name = models.TextField(blank=True, null=True)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='XOF')
    description = models.TextField(blank=True, null=True)
    shop = models.ForeignKey("core.Shop", models.CASCADE, related_name="products")

    slug = models.CharField(unique=True, max_length=255)
    weight = models.DecimalField(
        verbose_name="weight in kilograms", max_digits=6, decimal_places=3
    )
    available_units = models.PositiveIntegerField(null=True)
    categories = models.ManyToManyField('core.Category', related_name='products')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + "-" + secrets.token_urlsafe(2)
        super().save(*args, **kwargs)

    @cached_property
    def similar(self):
        return Product.objects.prefetch_related("images").filter(
            ~Q(pk=self.pk) & Q(shop=self.shop)
        )[0:4]

    @cached_property
    def currency_iso(self):
        return self.shop.currency_iso

    class Meta:
        managed = True
        db_table = "products"
