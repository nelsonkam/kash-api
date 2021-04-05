import secrets
from datetime import timedelta, date
from urllib import parse

from django.conf import settings
from django.db import models
from djmoney.contrib.exchange.models import convert_money
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from core.models.base import BaseModel
from core.utils import money_to_dict
from core.utils.payment import rave_request
from kash.models import Transaction


class VirtualCard(BaseModel):
    external_id = models.CharField(max_length=255, blank=True)
    service = models.CharField(max_length=255, default='rave')
    nickname = models.CharField(max_length=255)
    profile = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE)

    @property
    def issuance_cost(self):
        return Money(1000, 'XOF')

    def purchase(self, initial_amount, phone, gateway):
        return Transaction.objects.request(**{
            'obj': self,
            'name': self.profile.name,
            'amount': int(initial_amount) + self.issuance_cost.amount,
            'phone': phone,
            'gateway': gateway,
            'initiator': self.profile.user
        })

    def create_external(self, amount, **kwargs):
        # if settings.DEBUG:
        #     self.external_id = secrets.token_urlsafe(20)
        #     self.save()
        #     return
        initial_usd = convert_money(amount, 'USD')
        print(initial_usd)
        resp = rave_request('POST', '/virtual-cards', {
            'currency': 'USD',
            'amount': float(initial_usd.amount),
            'billing_name': self.profile.name or "John Doe",
            'debit_currency': 'NGN',
            'callback_url': "https://kweek-api.ngrok.io/kash/virtual-cards/txn_callback/"
        }).json()
        if resp.get('data'):
            self.external_id = resp.get('data').get('id')
            self.save()
        else:
            raise Exception(f"Card creation failed: {resp.get('message')}")


    @property
    def card_details(self):
        if not self.external_id:
            return None

        # if settings.DEBUG:
        #     return {
        #         "id": "7dc7b98c-7f6d-48f3-9b31-859a145c8085",
        #         "account_id": 65637,
        #         "amount": "20.00",
        #         "currency": "USD",
        #         "card_hash": "7dc7b98c-7f6d-48f3-9b31-859a145c8085",
        #         "card_pan": "5366130719043293",
        #         "masked_pan": "536613*******3293",
        #         "city": "Lekki",
        #         "state": "Lagos",
        #         "address_1": "19, Olubunmi Rotimi",
        #         "address_2": None,
        #         "zip_code": "23401",
        #         "cvv": "267",
        #         "expiration": "2023-01",
        #         "send_to": None,
        #         "bin_check_name": None,
        #         "card_type": "mastercard",
        #         "name_on_card": "Jermaine Graham",
        #         "created_at": "2020-01-17T18:31:48.97Z",
        #         "is_active": True,
        #         "callback_url": "https://your-callback-url.com/"
        #     }
        resp = rave_request('GET', f'/virtual-cards/{self.external_id}')

        return resp.json().get("data")



    def get_transactions(self):
        if not self.external_id:
            return None
        # if settings.DEBUG:
        #     return [
        #         {
        #             "id": 39250,
        #             "amount": 25000,
        #             "fee": 0,
        #             "product": "Card Transactions",
        #             "gateway_reference_details": "Card Withdrawal ",
        #             "reference": "CF-BARTER-20200113051758201204",
        #             "response_code": 5,
        #             "gateway_reference": "536613*******6517",
        #             "amount_confirmed": 0,
        #             "narration": "Card Withdrawal",
        #             "indicator": "D",
        #             "created_at": "2020-01-13T05:17:58.777Z",
        #             "status": "Successful",
        #             "response_message": "Transaction was Successful",
        #             "currency": "NGN"
        #         },
        #         {
        #             "id": 39248,
        #             "amount": 25000,
        #             "fee": 0,
        #             "product": "Card Transactions",
        #             "gateway_reference_details": "Card Withdrawal ",
        #             "reference": "CF-BARTER-20200113051659648286",
        #             "response_code": 5,
        #             "gateway_reference": "536613*******6517",
        #             "amount_confirmed": 0,
        #             "narration": "Card Withdrawal",
        #             "indicator": "D",
        #             "created_at": "2020-01-13T05:16:59.197Z",
        #             "status": "Successful",
        #             "response_message": "Transaction was Successful",
        #             "currency": "NGN"
        #         },
        #         {
        #             "id": 39246,
        #             "amount": 50000,
        #             "fee": 0,
        #             "product": "Card Funding",
        #             "gateway_reference_details": "38c9201a-fcb2-48fd-875e-6494ed79a6bb",
        #             "reference": "CF-BARTER-20200113042055432113",
        #             "response_code": 5,
        #             "gateway_reference": "536613*******6517",
        #             "amount_confirmed": 0,
        #             "narration": "Card Funding",
        #             "indicator": "C",
        #             "created_at": "2020-01-13T04:20:55.597Z",
        #             "status": "Successful",
        #             "response_message": "Transaction was Successful",
        #             "currency": "NGN"
        #         },
        #         {
        #             "id": 39244,
        #             "amount": 200000,
        #             "fee": 0,
        #             "product": "Card Funding",
        #             "gateway_reference_details": "38c9201a-fcb2-48fd-875e-6494ed79a6bb",
        #             "reference": "CF-BARTER-20200113041736563749",
        #             "response_code": 5,
        #             "gateway_reference": "536613*******6517",
        #             "amount_confirmed": 0,
        #             "narration": "Card Funding",
        #             "indicator": "C",
        #             "created_at": "2020-01-13T04:17:36.257Z",
        #             "status": "Successful",
        #             "response_message": "Transaction was Successful",
        #             "currency": "NGN"
        #         },
        #         {
        #             "id": 39242,
        #             "amount": 100000,
        #             "fee": 0,
        #             "product": "Card Funding",
        #             "gateway_reference_details": "38c9201a-fcb2-48fd-875e-6494ed79a6bb",
        #             "reference": "CF-BARTER-20200113041558850052",
        #             "response_code": 5,
        #             "gateway_reference": "536613*******6517",
        #             "amount_confirmed": 0,
        #             "narration": "Card Funding",
        #             "indicator": "C",
        #             "created_at": "2020-01-13T04:15:58.107Z",
        #             "status": "Successful",
        #             "response_message": "Transaction was Successful",
        #             "currency": "NGN"
        #         },
        #         {
        #             "id": 39240,
        #             "amount": 100000,
        #             "fee": 0,
        #             "product": "Card Funding",
        #             "gateway_reference_details": "38c9201a-fcb2-48fd-875e-6494ed79a6bb",
        #             "reference": "CF-BARTER-20200113041420718064",
        #             "response_code": 5,
        #             "gateway_reference": "536613*******6517",
        #             "amount_confirmed": 0,
        #             "narration": "Card Funding",
        #             "indicator": "C",
        #             "created_at": "2020-01-13T04:14:20.273Z",
        #             "status": "Successful",
        #             "response_message": "Transaction was Successful",
        #             "currency": "NGN"
        #         },
        #         {
        #             "id": 39227,
        #             "amount": 50000,
        #             "fee": 0,
        #             "product": "Card Funding",
        #             "gateway_reference_details": "38c9201a-fcb2-48fd-875e-6494ed79a6bb",
        #             "reference": "CF-BARTER-20200112054622949312",
        #             "response_code": 5,
        #             "gateway_reference": "536613*******6517",
        #             "amount_confirmed": 0,
        #             "narration": "Card Funding",
        #             "indicator": "C",
        #             "created_at": "2020-01-12T17:46:22.543Z",
        #             "status": "Successful",
        #             "response_message": "Transaction was Successful",
        #             "currency": "NGN"
        #         },
        #         {
        #             "id": 39226,
        #             "amount": 250,
        #             "fee": 0,
        #             "product": "Card Issuance Fee",
        #             "gateway_reference_details": "Card Issuance fee",
        #             "reference": "CF-BARTER-20200112054621157627",
        #             "response_code": 5,
        #             "gateway_reference": "selma FLW",
        #             "amount_confirmed": 0,
        #             "narration": "Card Issuance Fee",
        #             "indicator": "D",
        #             "created_at": "2020-01-12T17:46:21.84Z",
        #             "status": "Successful",
        #             "response_message": "Transaction was Successful",
        #             "currency": "NGN"
        #         },
        #         {
        #             "id": 39225,
        #             "amount": 50000,
        #             "fee": 0,
        #             "product": "Card Funding Debit",
        #             "gateway_reference_details": "Card Funding Transfers",
        #             "reference": "CF-BARTER-20200112054618252652",
        #             "response_code": 5,
        #             "gateway_reference": "selma FLW",
        #             "amount_confirmed": 0,
        #             "narration": None,
        #             "indicator": "D",
        #             "created_at": "2020-01-12T17:46:18.95Z",
        #             "status": "Successful",
        #             "response_message": "Transaction was Successful",
        #             "currency": "NGN"
        #         }
        #     ]

        query = {
            'from': (self.created_at - timedelta(days=90)).date().isoformat(),
            'to': date.today().isoformat(),
            'size': 1000,
            'index': 0
        }

        resp = rave_request('GET', f'/virtual-cards/{self.external_id}/transactions?{parse.urlencode(query)}')
        return resp.json().get("data")

