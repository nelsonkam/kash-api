from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from core.models.base import BaseModel, generate_uid



class Cart(BaseModel):
    uid = models.CharField(unique=True, max_length=40, default=generate_uid)
    products = models.ManyToManyField('core.Product', through='core.CartItem')
    paid = models.BooleanField(default=False)
    shop = models.ForeignKey("core.Shop", null=True, on_delete=models.CASCADE)

    @property
    def shops(self):
        from core.models import Shop

        return Shop.objects.filter(products__in=self.products.all()).distinct()

    @property
    def total(self):
        total = sum([item.total for item in self.items.all()])
        return Money(0, self.shop.currency_iso) if total == 0 else total

    class Meta:
        managed = True
        db_table = "carts"


class CartItem(BaseModel):
    quantity = models.IntegerField()
    cart = models.ForeignKey("core.Cart", models.CASCADE, related_name="items")
    product = models.ForeignKey("core.Product", models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='XOF')

    @property
    def total(self):
        return self.price * self.quantity

    class Meta:
        managed = True
        db_table = "cart_items"
