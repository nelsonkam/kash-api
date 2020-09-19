from decimal import Decimal

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models.base import BaseModel, generate_ref_id
from django.db import models

from core.utils import slack


def generate_affiliate_code():
    return generate_ref_id("A-", 4)


class AffiliateAgent(BaseModel):
    user = models.OneToOneField("core.User", on_delete=models.CASCADE, related_name="affiliate")
    code = models.CharField(max_length=10, default=generate_affiliate_code, unique=True)
    momo_number = models.CharField(max_length=255, null=True)
    avatar_url = models.URLField(blank=True)
    commission = models.DecimalField(max_digits=6, decimal_places=5, default=Decimal(0.08))

    @property
    def order_count(self):
        return self.orders.count()

    @property
    def orders(self):
        from core.models import Order
        return Order.objects.filter(shop__affiliate=self)

    @property
    def balance(self):
        return sum([order.affiliate_earnings for order in self.orders.all()])

    class Meta:
        db_table = "affiliate_agents"

@receiver(post_save, sender=AffiliateAgent)
def notify_slack(sender, instance, created, **kwargs):
    if created:
        message = [
            {
                "fallback": f"New Partner on Kweek!💪🏾",
                "color": "#30BCED",
                "pretext": "New Partner on Kweek!💪🏾",
                "fields": [
                    {"title": "Name", "value": instance.user.name, "short": True},
                    {
                        "title": "Phone Number",
                        "value": instance.user.phone_number,
                        "short": True,
                    },
                    {
                        "title": "Commission",
                        "value": f"{round(instance.commission * 100)}%",
                        "short": True,
                    },
                ],
            }
        ]
        slack.send_message(message, "#test" if settings.DEBUG else "#notifications")
