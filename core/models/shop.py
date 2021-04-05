from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money

from core.models.base import BaseModel
from core.utils import notify
from core.utils.notify import tg_bot


class Shop(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    username = models.CharField(unique=True, max_length=255)
    avatar_url = models.URLField(blank=True, null=True)
    cover_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True)
    country_code = models.CharField(max_length=10, default="BJ")
    currency_iso = models.CharField(max_length=10, default="EUR")
    user = models.ForeignKey('core.User', models.CASCADE, related_name="shops")
    affiliate = models.ForeignKey('core.AffiliateAgent', on_delete=models.SET_NULL, null=True, related_name="shops")
    domains = ArrayField(models.CharField(max_length=255), default=list)

    @property
    def balance(self):
        earnings = [convert_money(order.earnings, self.currency_iso) for order in self.orders.all()]
        if sum(earnings) == 0:
            return Money(0, self.currency_iso)
        return sum(earnings)

    @property
    def order_count(self):
        return self.orders.count()

    class Meta:
        managed = True
        db_table = 'shops'


@receiver(post_save, sender=Shop)
def notify_slack(sender, instance, created, **kwargs):
    if created:
        tg_bot.send_message(chat_id=settings.TG_CHAT_ID, text=f"""
        New shop created on Kweek!💪🏾

        Nom: {instance.name}
        Lien: https://{instance.username}.kweek.shop
        Tel: {instance.phone_number}

        {"_Ceci est un message test._" if settings.DEBUG else ""}
        """)
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
        notify.send_message(message, "#test" if settings.DEBUG else "#notifications")


@receiver(post_save, sender=Shop)
def add_shop_design(sender, instance, created, **kwargs):
    from core.models import ShopDesign

    if created:
        ShopDesign.objects.create(
            tagline="Découvrez nos meilleurs produits et collections", hero_cta="Shoppez maintenant", shop=instance
        )


@receiver(post_save, sender=Shop)
def add_shipping_profiles(sender, instance, created, **kwargs):
    from core.models import ShippingProfile

    if created:
        profile = ShippingProfile.objects.filter(name__icontains="futurix").first()
        profile.shops.add(instance)
