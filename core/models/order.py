from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    shipping_option = models.JSONField(blank=True, null=True)
    payment_method = models.CharField(
        max_length=10, default=PaymentMethod.card, choices=PaymentMethod.choices
    )

    @property
    def commission(self):
        return round(self.total * 0.08)

    @property
    def earnings(self):
        return self.total - self.commission

    @property
    def affiliate_earnings(self):
        return self.shipping_fees * self.shop.affiliate.commission

    @property
    def shipping_fees(self):
        if self.shipping_option:
            return self.shipping_option.get("price").get("amount")
        return None

    @property
    def total(self):
        return sum([item.total for item in self.items.select_related("product")])

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
                        "value": f"{self.shipping_option.get('name')} ({self.shipping_fees} XOF)",
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

    @property
    def total(self):
        return self.product.price * self.quantity

    class Meta:
        managed = True
        db_table = "order_items"

