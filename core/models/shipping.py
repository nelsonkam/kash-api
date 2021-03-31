from django.db import models
from django.utils.module_loading import import_string
from djmoney.models.fields import MoneyField

from core.models.base import BaseModel
from core.utils import money_to_dict


class ShippingProfile(BaseModel):
    class ProfileTypes(models.TextChoices):
        manual = 'manual', "Manual"
        auto = 'auto', 'Auto'

    name = models.CharField(max_length=255)
    avatar_url = models.URLField(blank=True)
    shops = models.ManyToManyField('core.Shop')
    backend = models.CharField(max_length=255, blank=True)
    profile_type = models.CharField(max_length=255, choices=ProfileTypes.choices, default=ProfileTypes.manual)

    def get_rates(self, region, **kwargs):
        if self.profile_type == ShippingProfile.ProfileTypes.manual:
            zone = self.zones.filter(name=region).prefetch_related('shippingmethod_set').first()
            if not zone:
                return []
            return [{'name': method.name, 'description': method.description, 'price': money_to_dict(method.price)} for
                    method in
                    zone.shippingmethod_set.all()]
        elif self.profile_type == ShippingProfile.ProfileTypes.auto:
            backend_cls = import_string(self.backend)
            return backend_cls().get_rates(region, **kwargs)


class ShippingZone(BaseModel):
    name = models.CharField(max_length=255)
    profile = models.ForeignKey(ShippingProfile, on_delete=models.CASCADE, related_name='zones')


class ShippingMethod(BaseModel):
    name = models.CharField(max_length=255)
    zone = models.ForeignKey(ShippingZone, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='XOF')
