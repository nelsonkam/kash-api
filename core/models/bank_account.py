from django.conf import settings
from django.db import models

from core.models.base import BaseModel
from core.utils.payment import rave_request


class BankAccount(BaseModel):
    external_id = models.CharField(max_length=255, blank=True)
    account_bank = models.CharField(max_length=10)
    account_number = models.CharField(max_length=255)
    rave_subaccount_id = models.CharField(max_length=255, blank=True)
    service = models.CharField(max_length=15, blank=True)
    shop = models.OneToOneField("core.Shop", on_delete=models.CASCADE)

    def create_subaccount(self):
        if self.external_id:
            resp = rave_request("PUT", f"/subaccounts/{self.external_id}", {
                "account_bank": self.account_bank,
                "account_number": self.account_number,
                "business_name": self.shop.name,
                "country": self.shop.country_code,
                "business_mobile": self.shop.phone_number,
                "business_contact": self.shop.user.name,
                "business_email": self.shop.email,
                "split_value": settings.KWEEK_COMMISSION_RATIO,
                "split_type": "percentage",
                "meta": {
                    "shop_id": self.shop.pk
                }
            })
        else:
            resp = rave_request("POST", "/subaccounts", {
                "account_bank": self.account_bank,
                "account_number": self.account_number,
                "business_name": self.shop.name,
                "country": self.shop.country_code,
                "business_mobile": self.shop.phone_number,
                "business_contact": self.shop.user.name,
                "business_email": self.shop.email,
                "split_value": settings.KWEEK_COMMISSION_RATIO,
                "split_type": "percentage",
                "meta": {
                    "shop_id": self.shop.pk
                }
            })
        if resp.status_code == 200:
            data = resp.json().get("data")
            self.external_id = data.get('id')
            self.rave_subaccount_id = data.get('subaccount_id')
            self.service = "rave"
            self.save()
        else:
            print(resp, resp.text)
            raise Exception("Couldn't create subaccount.")
