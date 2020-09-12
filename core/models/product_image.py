from django.db import models

from core.models.base import BaseModel


class ProductImage(BaseModel):
    url = models.URLField(null=True)
    product = models.ForeignKey('Product', models.CASCADE, related_name="images")

    class Meta:
        managed = True
        db_table = 'product_images'
