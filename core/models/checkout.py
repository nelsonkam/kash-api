
from django.db import models
from django.utils.functional import cached_property
from djmoney.contrib.exchange.models import convert_money
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from core.models.base import BaseModel, generate_uid, PaymentMethod, generate_ref_id
from core.utils.payment import Payment

def generate_checkout_ref():
    return generate_ref_id("C-")

class Checkout(BaseModel):
    customer = models.ForeignKey('core.Customer', models.CASCADE)
    cart = models.ForeignKey('core.Cart', models.CASCADE)
    country = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    address = models.TextField()
    ref_id = models.CharField(unique=True, max_length=40, default=generate_checkout_ref)
    paid = models.BooleanField(default=False)
    uid = models.CharField(unique=True, max_length=40, default=generate_uid)
    payment_method = models.CharField(max_length=10, default=PaymentMethod.card, choices=PaymentMethod.choices)
    shipping_fees = MoneyField(max_digits=14, decimal_places=2, default_currency='XOF', null=True)
    shipping_profile = models.ForeignKey('core.ShippingProfile', models.CASCADE, null=True)
    zone = models.CharField(max_length=255, blank=True)

    @cached_property
    def shop(self):
        return self.cart.shop

    @property
    def total(self):
        shipping_fees = convert_money(self.shipping_fees or Money(0, self.shop.currency_iso), self.shop.currency_iso)
        return self.cart.total + shipping_fees

    def pay(self, **kwargs):
        from core.models import Order, CartItem
        
        if not self.paid and Payment.verify_transaction(self.payment_method, **kwargs):
            cart = self.cart
            order = Order.objects.create(
                customer=self.customer,
                country=self.country,
                city=self.city,
                address=self.address,
                shipping_fees=self.shipping_fees,
                shipping_profile=self.shipping_profile,
                payment_method=self.payment_method,
                zone=self.zone,
                shop=self.shop
            )
            items = CartItem.objects.filter(cart=cart, product__shop=self.shop).select_related("product").all()
            for item in items:
                order.items.create(quantity=item.quantity, product=item.product, price=item.price)
            order.notify()
            self.paid = True
            cart.paid = True
            cart.save()
            self.save()

    class Meta:
        managed = True
        db_table = 'checkouts'
