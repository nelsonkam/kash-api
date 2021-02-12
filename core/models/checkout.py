from django.db import models

from core.models.base import BaseModel, generate_uid, PaymentMethod, generate_ref_id
from core.utils.payment import Payment

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

    def pay(self, **kwargs):
        from core.models import Shop, Checkout, Order, CartItem
        
        if not self.paid and Payment.verify_transaction(self.payment_method, **kwargs):
            cart = self.cart
            for shop in cart.shops.all():
                order = Order.objects.create(
                    customer=self.customer,
                    country=self.country,
                    city=self.city,
                    address=self.address,
                    shipping_option=self.shipping_option,
                    payment_method=self.payment_method,
                    shop=shop
                )
                items = CartItem.objects.filter(cart=cart, product__shop=shop).select_related("product").all()
                for item in items:
                    order.items.create(quantity=item.quantity, product=item.product)
                order.notify()
            self.paid = True
            cart.paid = True
            cart.save()
            self.save()

    class Meta:
        managed = True
        db_table = 'checkouts'
