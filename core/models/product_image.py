from django.db import models

from core.models.base import BaseModel


class ProductImage(BaseModel):
    url = models.URLField()
    product = models.ForeignKey('Product', models.CASCADE)

    class Meta:
        managed = True
        db_table = 'product_images'
