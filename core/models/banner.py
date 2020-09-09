from django.db import models

from core.models.base import BaseModel


class Banner(BaseModel):
    link = models.TextField()
    image_url = models.TextField()


    class Meta:
        managed = True
        db_table = 'banners'
