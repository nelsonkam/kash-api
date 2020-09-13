from django.db import models

from core.models.base import BaseModel, generate_uid, PaymentMethod, generate_ref_id


def generate_checkout_ref():
    return generate_ref_id("C-")

class Checkout(BaseModel):
    customer = models.ForeignKey('core.Customer', models.CASCADE)
    cart = models.ForeignKey('core.Cart', models.CASCADE)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.TextField()
    ref_id = models.CharField(unique=True, max_length=40, default=generate_checkout_ref)
    paid = models.BooleanField(default=False)
    uid = models.CharField(unique=True, max_length=40, default=generate_uid)
    shipping_option = models.JSONField(blank=True, null=True)
    payment_method = models.CharField(max_length=10, default=PaymentMethod.card, choices=PaymentMethod.choices)

    def shipping_fees(self):
        if self.shipping_option:
            return self.shipping_option.get("price").get("amount")
        return None

    def total(self):
        return self.cart.total() + (self.shipping_fees() or 0)

    class Meta:
        managed = True
        db_table = 'checkouts'
