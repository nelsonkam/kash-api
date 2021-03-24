from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from core.models.base import BaseModel, PaymentMethod, generate_ref_id
from django.db import models

from core.utils import slack
from core.utils.sms import send_sms


def generate_order_id():
    return generate_ref_id("O-")


class Order(BaseModel):
    shop = models.ForeignKey(
        "core.Shop", on_delete=models.CASCADE, related_name="orders"
    )
    customer = models.ForeignKey("core.Customer", models.CASCADE)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.TextField()
    ref_id = models.CharField(unique=True, max_length=40, default=generate_order_id)
    payment_method = models.CharField(
        max_length=10, default=PaymentMethod.card, choices=PaymentMethod.choices
    )
    shipping_fees = MoneyField(max_digits=14, decimal_places=2, default_currency='XOF', null=True)
    shipping_profile = models.ForeignKey('core.ShippingProfile', models.CASCADE, null=True)
    zone = models.CharField(max_length=255, blank=True)

    @property
    def commission(self):
        if self.payment_method == PaymentMethod.cash:
            return Money(0, self.shop.currency_iso)
        return self.total * settings.KWEEK_COMMISSION_RATIO

    @property
    def earnings(self):
        return self.total - self.commission

    @property
    def total(self):
        total = sum([item.total for item in self.items.select_related("product")])
        return Money(0, self.shop.currency_iso) if total == 0 else total

    def notify(self):
        self.notify_shop()
        self.notify_slack()

    def notify_shop(self):
        message = f"Nouvelle commande d'une valeur de {self.total} XOF pour votre boutique {self.shop.name}. Reference: {self.ref_id}"
        send_sms(self.shop.user.phone_number, message)

    def notify_slack(self):
        message = [
            {
                "fallback": f"Nouvelle commande sur Kweek!💪🏾",
                "color": "#30BCED",
                "pretext": "Nouvelle commande sur Kweek!💪🏾",
                "fields": [
                    {
                        "title": "Boutique",
                        "value": f"{self.shop.name} ({self.shop.username})",
                        "short": True,
                    },
                    {
                        "title": "Nom du client",
                        "value": self.customer.name,
                        "short": True,
                    },
                    {"title": "Total", "value": f"{self.total} XOF", "short": True},
                    {
                        "title": "Commission",
                        "value": f"{self.commission} XOF",
                        "short": True,
                    },
                    {
                        "title": "Option de livraison",
                        "value": f"{self.shipping_profile.name} ({self.shipping_fees})",
                        "short": True,
                    },
                    {
                        "title": "Mode de paiement",
                        "value": f"{self.payment_method}",
                        "short": True,
                    },
                    {"title": "Reference", "value": self.ref_id, "short": True},
                    {
                        "title": "Contact",
                        "value": self.customer.phone_number,
                        "short": True,
                    },
                    {
                        "title": "Addresse",
                        "value": f"{self.address}\n{self.city}, {self.country}",
                    },
                ],
            }
        ]
        slack.send_message(message, "#test" if settings.DEBUG else "#notifications")

    class Meta:
        managed = True
        db_table = "orders"


class OrderItem(BaseModel):
    quantity = models.IntegerField()
    order = models.ForeignKey("core.Order", models.CASCADE, related_name="items")
    product = models.ForeignKey("core.Product", models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='XOF')

    @property
    def total(self):
        return self.price * self.quantity

    class Meta:
        managed = True
        db_table = "order_items"

