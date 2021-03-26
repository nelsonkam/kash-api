from django.db import models

from core.models.base import BaseModel


class ShopDesign(BaseModel):
    shop = models.OneToOneField("core.Shop", on_delete=models.CASCADE, related_name="design")
    tagline = models.CharField(max_length=225)
    hero_cta = models.CharField(max_length=100)
    instagram_link = models.URLField(blank=True)
    facebook_link = models.URLField(blank=True)
    whatsapp_link = models.URLField(blank=True)
    theme = models.CharField(max_length=255, default='storefront')
    color = models.CharField(max_length=20, default='black')
    language = models.CharField(max_length=10, default="fr")
