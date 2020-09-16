from django.db import models

from core.models.base import BaseModel


class Shop(BaseModel):
    name = models.CharField(max_length=255)
    username = models.CharField(unique=True, max_length=255)
    avatar_url = models.URLField(blank=True, null=True)
    cover_url = models.URLField(blank=True, null=True)
    whatsapp_number = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=255)
    user = models.ForeignKey('core.User', models.CASCADE, related_name="shops")
    affiliate = models.ForeignKey('core.AffiliateAgent', on_delete=models.SET_NULL, null=True, related_name="shops")

    @property
    def balance(self):
        return sum([order.earnings for order in self.orders.all()])

    @property
    def order_count(self):
        return self.orders.count()

    class Meta:
        managed = True
        db_table = 'shops'
