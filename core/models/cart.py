from django.db import models


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

    def total(self):
        return sum([item.total() for item in self.items.select_related("product")])

    class Meta:
        managed = True
        db_table = "carts"


class CartItem(BaseModel):
    quantity = models.IntegerField()
    cart = models.ForeignKey("core.Cart", models.CASCADE, related_name="items")
    product = models.ForeignKey("core.Product", models.CASCADE)

    def total(self):
        return self.product.price * self.quantity

    class Meta:
        managed = True
        db_table = "cart_items"
