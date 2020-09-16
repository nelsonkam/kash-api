from core.models.base import BaseModel, generate_ref_id
from django.db import models


def generate_affiliate_code():
    return generate_ref_id("A-", 4)


class AffiliateAgent(BaseModel):
    user = models.OneToOneField("core.User", on_delete=models.CASCADE, related_name="affiliate")
    code = models.CharField(max_length=10, default=generate_affiliate_code)
    momo_number = models.CharField(max_length=255, null=True)
    avatar_url = models.URLField(blank=True)

    @property
    def order_count(self):
        return self.orders.count()

    @property
    def orders(self):
        from core.models import Order
        return Order.objects.filter(shop__affiliate=self)

    @property
    def balance(self):
        return sum([order.shipping_fees * 0.08 for order in self.orders])

    class Meta:
        db_table = "affiliate_agents"
