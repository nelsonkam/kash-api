import secrets

from django.db import models
from django.utils.text import slugify

from core.models.base import BaseModel


class Category(BaseModel):
    name = models.TextField(unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + secrets.token_urlsafe(2)
        super().save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'categories'
