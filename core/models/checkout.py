from django.db import models

from core.models.base import BaseModel, generate_uid


class Checkout(BaseModel):
    customer = models.ForeignKey('core.Customer', models.CASCADE)
    cart = models.ForeignKey('core.Cart', models.CASCADE)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.TextField()
    uid = models.CharField(unique=True, max_length=40, default=generate_uid)
    shipping_option = models.JSONField(blank=True, null=True)

    def total(self):
        if hasattr(self, 'shipping_option'):
            option = self.shipping_option
            return self.cart.total() + option.get("price").get("amount")
        return self.cart.total()

    class Meta:
        managed = True
        db_table = 'checkouts'
