import secrets
from datetime import timedelta, date
from urllib import parse

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver
from djmoney.contrib.exchange.models import convert_money
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from core.models.base import BaseModel
from core.utils.payment import rave_request, rave2_request
from kash.signals import transaction_status_changed
from kash.utils import TransactionStatusEnum, TransactionType


class VirtualCard(BaseModel):
    external_id = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    service = models.CharField(max_length=255, default='rave')
    nickname = models.CharField(max_length=255)
    profile = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE)

    @property
    def issuance_cost(self):
        return Money(1000, 'XOF')

    def purchase(self, initial_amount, phone, gateway):
        from kash.models import Transaction
        return Transaction.objects.request(**{
            'obj': self,
            'name': self.profile.name,
            'amount': int(initial_amount) + self.issuance_cost.amount,
            'phone': phone,
            'gateway': gateway,
            'initiator': self.profile.user
        })

    def create_external(self, amount, **kwargs):
        if settings.DEBUG:
            self.external_id = secrets.token_urlsafe(20)
            self.save()
            return
        initial_usd = convert_money(amount, 'USD')
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

        if settings.DEBUG:
            return {
                "id": "7dc7b98c-7f6d-48f3-9b31-859a145c8085",
                "account_id": 65637,
                "amount": "20.00",
                "currency": "USD",
                "card_hash": "7dc7b98c-7f6d-48f3-9b31-859a145c8085",
                "card_pan": "5366130719043293",
                "masked_pan": "536613*******3293",
                "city": "Lekki",
                "state": "Lagos",
                "address_1": "19, Olubunmi Rotimi",
                "address_2": None,
                "zip_code": "23401",
                "cvv": "267",
                "expiration": "2023-01",
                "send_to": None,
                "bin_check_name": None,
                "card_type": "mastercard",
                "name_on_card": "Jermaine Graham",
                "created_at": "2020-01-17T18:31:48.97Z",
                "is_active": True,
                "callback_url": "https://your-callback-url.com/"
            }
        resp = rave_request('GET', f'/virtual-cards/{self.external_id}')

        return resp.json().get("data")

    def get_transactions(self):
        if not self.external_id:
            return None
        if settings.DEBUG:
            return [
                {
                    "id": 39250,
                    "amount": 25,
                    "fee": 0,
                    "product": "Card Transactions",
                    "gateway_reference_details": "Card Withdrawal ",
                    "reference": "CF-BARTER-20200113051758201204",
                    "response_code": 5,
                    "gateway_reference": "536613*******6517",
                    "amount_confirmed": 0,
                    "narration": "Card Withdrawal",
                    "indicator": "D",
                    "created_at": "2020-01-13T05:17:58.777Z",
                    "status": "Successful",
                    "response_message": "Transaction was Successful",
                    "currency": "USD"
                },
            ]

        query = {
            'from': (self.created_at - timedelta(days=90)).date().isoformat(),
            'to': date.today().isoformat(),
            'size': 10,
            'index': 1
        }
        resp = rave_request('GET', f'/virtual-cards/{self.external_id}/transactions?{parse.urlencode(query)}')
        return resp.json().get('data')
        # data = {
        #     "FromDate": (self.created_at - timedelta(days=90)).date().isoformat(),
        #     "ToDate": date.today().isoformat(),
        #     "PageIndex": 0,
        #     "PageSize": 20,
        #     "CardId": self.external_id,
        #     "secret_key": settings.RAVE_SECRET_KEY
        # }
        # resp = rave2_request("POST", '/services/virtualcards/transactions', data)
        # return resp.json().get("Statements") or []

    def fund(self, amount, phone, gateway):
        from kash.models import Transaction
        return Transaction.objects.request(**{
            'obj': self,
            'name': self.profile.name,
            'amount': amount,
            'phone': phone,
            'gateway': gateway,
            'initiator': self.profile.user
        })

    def fund_external(self, amount):
        if not self.external_id:
            return None
        if settings.DEBUG:
            return

        data = {
            'amount': float(amount.amount),
            'debit_currency': "NGN"
        }

        return rave_request("POST", f'/virtual-cards/{self.external_id}/fund', data)

    def freeze(self):
        if not self.external_id:
            return None
        if not settings.DEBUG:
            rave_request("PUT", f'/virtual-cards/{self.external_id}/status/block')
        self.is_active = False
        self.save()
        return

    def unfreeze(self):
        if not self.external_id:
            return None
        if not settings.DEBUG:
            rave_request("PUT", f'/virtual-cards/{self.external_id}/status/unblock')
        self.is_active = True
        self.save()
        return

    def withdraw(self, amount):
        from kash.models import Transaction
        if not self.external_id:
            return None
        if not settings.DEBUG:
            rave_request("POST", f'/virtual-cards/{self.external_id}/withdraw', {
                'amount': int(amount.amount)
            })
        withdraw_amount = convert_money(amount, "XOF") - Money(200, "XOF") # withdrawal fee
        payout_method = self.profile.payout_methods.first()
        txn = Transaction.objects.request(
            obj=self,
            name=self.profile.name,
            amount=withdraw_amount,
            phone=payout_method.phone,
            gateway=payout_method.gateway,
            initiator=self.profile.user,
            txn_type=TransactionType.payout
        )
        WithdrawalHistory.objects.create(txn_ref=txn.reference, card=self, amount=amount)
        return

    def terminate(self):
        if not self.external_id:
            return None
        if not settings.DEBUG:
            rave_request("PUT", f'/virtual-cards/{self.external_id}/terminate')
        self.external_id = None
        self.is_active = False
        self.save()
        return


class FundingHistory(BaseModel):
    txn_ref = models.CharField(max_length=255, unique=True)
    card = models.ForeignKey(VirtualCard, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=17, decimal_places=2, default_currency="XOF")


class WithdrawalHistory(BaseModel):
    txn_ref = models.CharField(max_length=255, unique=True)
    card = models.ForeignKey(VirtualCard, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=17, decimal_places=2, default_currency="XOF")


@receiver(transaction_status_changed)
def fund_card(sender, **kwargs):
    txn = kwargs.pop("transaction")
    vcard_type = ContentType.objects.get_for_model(VirtualCard)

    if txn.content_type == vcard_type and txn.status == TransactionStatusEnum.success.value:
        card = txn.content_object
        if card.external_id and not FundingHistory.objects.filter(txn_ref=txn.reference, card=card).exists():
            amount = convert_money(txn.amount, "USD")
            try:
                card.fund_external(amount)
                FundingHistory.objects.create(txn_ref=txn.reference, card=card, amount=amount)
            except:
                txn.refund()
