from django.db import models

from core.models.base import BaseModel, generate_uid


class Cart(BaseModel):
    uid = models.CharField(unique=True, max_length=40, default=generate_uid)

    class Meta:
        managed = True
        db_table = "carts"


class CartItem(BaseModel):
    quantity = models.IntegerField()
    cart = models.ForeignKey("core.Cart", models.CASCADE)
    product = models.ForeignKey("core.Product", models.CASCADE)

    class Meta:
        managed = True
        db_table = "cart_items"
