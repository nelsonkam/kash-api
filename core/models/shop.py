from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models.base import BaseModel
from core.utils import slack


class Shop(BaseModel):
    name = models.CharField(max_length=255)
    username = models.CharField(unique=True, max_length=255)
    avatar_url = models.URLField(blank=True, null=True)
    cover_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True)
    country_code = models.CharField(max_length=10, default="BJ")
    currency_iso = models.CharField(max_length=10, default="XOF")
    user = models.ForeignKey('core.User', models.CASCADE, related_name="shops")
    affiliate = models.ForeignKey('core.AffiliateAgent', on_delete=models.SET_NULL, null=True, related_name="shops")
    domains = ArrayField(models.CharField(max_length=255), default=list)

    @property
    def balance(self):
        return sum([order.earnings for order in self.orders.all()])

    @property
    def order_count(self):
        return self.orders.count()

    class Meta:
        managed = True
        db_table = 'shops'


@receiver(post_save, sender=Shop)
def notify_slack(sender, instance, created, **kwargs):
    if created:
        message = [
            {
                "fallback": f"New shop created on Kweek!💪🏾",
                "color": "#30BCED",
                
                "pretext": "New shop created on Kweek!💪🏾",
                "fields": [
                    {"title": "Name", "value": instance.name, "short": True},
                    {"title": "Link", "value": f"https://{instance.username}.kweek.shop", "short": True},
                    {
                        "title": "Phone Number",
                        "value": instance.phone_number,
                        "short": True,
                    },
                ],
            }
        ]
        slack.send_message(message, "#test" if settings.DEBUG else "#notifications")
