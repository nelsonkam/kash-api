import secrets

from django.db import models
from django.utils.functional import cached_property
from django.utils.text import slugify

from core.models.base import BaseModel


class Category(BaseModel):
    name = models.TextField()
    slug = models.SlugField()
    shop = models.ForeignKey('core.Shop', models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def product_count(self):
        return self.products.count()

    class Meta:
        managed = True
        db_table = 'categories'
        constraints = [
            models.UniqueConstraint(fields=['shop', 'slug'], name='unique_category_slug_per_shop')
        ]
