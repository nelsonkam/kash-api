import secrets

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core import signing
from django.db import models
from django.utils import timezone
from djmoney.contrib.exchange.models import convert_money
from djmoney.forms import MoneyField
from djmoney.money import Money
from itsdangerous import URLSafeTimedSerializer

from core.models.base import BaseModel, PaymentMethod


def generate_uid():
    return secrets.token_urlsafe(32)


class CheckoutSession(BaseModel):
    shop = models.ForeignKey('core.Shop', on_delete=models.CASCADE)
    uid = models.CharField(max_length=255, default=generate_uid)
    cart = models.ForeignKey('core.Cart', on_delete=models.CASCADE)
    paid_at = models.DateTimeField(null=True)
    cancel_url = models.URLField()
    order = models.OneToOneField('core.Order', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('core.User', on_delete=models.SET_NULL)
    transactions = GenericRelation('pay.Transaction')

    @property
    def session_id(self):
        return signing.dumps({'id': self.pk})

    @property
    def total(self):
        shipping_fees = convert_money(self.order.shipping_fees or Money(0, self.shop.currency_iso),
                                      self.shop.currency_iso)
        return self.cart.total + shipping_fees

    def pay(self, payload=None):
        from pay.models import Transaction

        if self.order.payment_method == PaymentMethod.momo:
            Transaction.objects.request(**{
                "amount": self.order.total.amount,
                "name": self.order.customer.name,
                "phone": payload.get('phone'),

            })
            Transaction.objects.request(
                amount=self.order.total.amount,
                name=self.order.customer.name,
                phone=payload.get('phone'),
                obj=self,
                gateway=payload.get('gateway')
            )

    def paid(self, **kwargs):
        self.order.notify()
        self.paid_at = timezone.now()
        self.cart.paid = True
        self.cart.save()
        self.save()
