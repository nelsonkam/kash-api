from core.models.base import BaseModel, PaymentMethod, generate_ref_id
from django.db import models

from core.utils.sms import send_sms


def generate_order_id():
    return generate_ref_id("O-")


class Order(BaseModel):
    shop = models.ForeignKey("core.Shop", on_delete=models.CASCADE)
    customer = models.ForeignKey("core.Customer", models.CASCADE)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.TextField()
    ref_id = models.CharField(unique=True, max_length=40, default=generate_order_id)
    shipping_option = models.JSONField(blank=True, null=True)
    payment_method = models.CharField(
        max_length=10, default=PaymentMethod.card, choices=PaymentMethod.choices
    )

    def total(self):
        return sum([item.total() for item in self.items.select_related("product")])

    def notify_shop(self):
        message = f"Nouvelle commande d'une valeur de {self.total()} XOF pour votre boutique {self.shop.name}. Reference: {self.ref_id}"
        send_sms(self.shop.user.phone_number, message)

    class Meta:
        managed = True
        db_table = "orders"


class OrderItem(BaseModel):
    quantity = models.IntegerField()
    order = models.ForeignKey("core.Order", models.CASCADE, related_name="items")
    product = models.ForeignKey("core.Product", models.CASCADE)

    def total(self):
        return self.product.price * self.quantity

    class Meta:
        managed = True
        db_table = "order_items"
