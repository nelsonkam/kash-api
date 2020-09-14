from django.db import models

from core.models.base import BaseModel


class Shop(BaseModel):
    name = models.CharField(max_length=255)
    username = models.CharField(unique=True, max_length=255)
    avatar_url = models.TextField(blank=True, null=True)
    cover_url = models.TextField(blank=True, null=True)
    whatsapp_number = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=255)
    user = models.ForeignKey('core.User', models.CASCADE, related_name="shops")

    @property
    def balance(self):
        return sum([order.earnings for order in self.order_set.all()])

    @property
    def order_count(self):
        return self.order_set.count()

    class Meta:
        managed = True
        db_table = 'shops'
