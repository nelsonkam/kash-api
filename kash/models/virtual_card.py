import secrets
import re
from datetime import timedelta, date
from urllib import parse

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver
from djmoney.contrib.exchange.models import convert_money
from djmoney.models.fields import MoneyField
from djmoney.money import Money, Currency
from stellar_sdk import TransactionBuilder

from core.models.base import BaseModel
from core.utils.payment import rave_request, rave2_request
from kash.signals import transaction_status_changed
from kash.utils import TransactionStatusEnum, TransactionType, Conversions, StellarHelpers


class VirtualCard(BaseModel):
    external_id = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    service = models.CharField(max_length=255, default='rave')
    nickname = models.CharField(max_length=255)
    profile = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE)

    @property
    def issuance_cost(self):
        return Money(0, 'XOF')

    def purchase(self, amount, usd_amount):
        from kash.models import Wallet
        if not hasattr(self.profile, "wallet"):
            Wallet.objects.create(profile=self.profile)

        converted_amount = Money(round(amount.amount / Conversions.get_usd_rate(), 7), "USD")

        self.profile.wallet.pay(converted_amount, "Achat de carte")
        self.create_external(Money(usd_amount, "USD"))

    def purchase_momo(self, amount, phone, gateway):
        from kash.models import Transaction, KashTransaction
        xof_amount = amount if amount.currency == Currency('XOF') else Conversions.get_xof_from_usd(amount)
        usd_amount = amount if amount.currency == Currency('USD') else Conversions.get_usd_from_xof(amount)

        txn = Transaction.objects.request(**{
            'obj': self,
            'name': self.profile.name,
            'amount': xof_amount + self.issuance_cost,
            'phone': phone,
            'gateway': gateway,
            'initiator': self.profile.user
        })
        KashTransaction.objects.create(
            amount=txn.amount,
            sender=self.profile,
            txn=txn,
            txn_ref=txn.reference,
            timestamp=txn.created,
            profile=self.profile,
            narration="Achat d'une carte virtuelle 💳",
            receiver=self,
            txn_type=KashTransaction.TxnType.debit,
        )
        FundingHistory.objects.create(txn_ref=txn.reference, card=self, amount=usd_amount, status='pending')
        return txn

    def create_external(self, usd_amount, **kwargs):
        if self.external_id:
            return

        if settings.DEBUG:
            self.external_id = secrets.token_urlsafe(20)
            self.save()
            return

        usd_balance = rave_request("GET", "/balances/USD").json().get('data').get('available_balance')
        debit_currency = 'NGN'
        if usd_amount.amount <= usd_balance - 5:
            debit_currency = 'USD'

        resp = rave_request('POST', '/virtual-cards', {
            'currency': 'USD',
            'amount': float(usd_amount.amount),
            'billing_name': self.profile.name or "John Doe",
            'debit_currency': debit_currency,
            'callback_url': "https://prod.mykash.africa/kash/virtual-cards/txn_callback/"
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
        rave2_request("POST", f'/cardservice/balance/{self.external_id}?seckey={settings.RAVE_SECRET_KEY}')
        resp = rave_request('GET', f'/virtual-cards/{self.external_id}')

        return resp.json().get("data")

    def get_statement(self):
        if settings.DEBUG:
            data = [{
                "date": "2021-05-09",
                "amount": "150.00",
                "type": "Debit",
                "balance_before": "30.00",
                "balance_after": "180.00",
                "merchant": "Funding"
            },{
                "date": "2021-05-08",
                "amount": "150.00",
                "type": "Credit",
                "balance_before": "30.00",
                "balance_after": "180.00",
                "merchant": "Funding"
            }]
        else:
            data = self.rave2_transactions() or []

        return [{**i, 'type': i.get('type').lower(), 'created_at': i.get('date'), 'status': "success", } for i in data]

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

        def format_reference(ref):
            if re.match(r'^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$', ref.upper()):
                return self.profile.name or 'Kash'
            return ref

        data = [{
            'status': item.get("status"),
            'indicator': item.get('indicator'),
            'gateway_reference_details': format_reference(item.get('gateway_reference_details')),
            'narration': item.get('narration') or item.get('product'),
            'amount': item.get('amount'),
            'fee': item.get('fee'),
            'currency': item.get('currency'),
            'created_at': item.get('created_at')
        } for item in self.rave_transactions()]
        return data

    def rave_transactions(self):
        query = {
            'from': (date.today() - timedelta(days=90)).isoformat(),
            'to': (date.today() + timedelta(days=1)),
            'size': 20,
            'index': 1
        }
        resp = rave_request('GET', f'/virtual-cards/{self.external_id}/transactions?{parse.urlencode(query)}')
        return resp.json().get('data')

    def rave2_transactions(self):
        data = {
            "FromDate": (self.created_at - timedelta(days=90)).date().isoformat(),
            "ToDate": (date.today() + timedelta(days=1)).isoformat(),
            "PageIndex": 0,
            "PageSize": 20,
            "CardId": self.external_id,
            "secret_key": settings.RAVE_SECRET_KEY
        }
        resp = rave2_request("POST", '/services/virtualcards/transactions', data)
        return resp.json().get("Statements")

    def fund_momo(self, amount, phone, gateway):
        from kash.models import Transaction, KashTransaction
        xof_amount = Conversions.get_xof_from_usd(amount)
        total_amount = xof_amount + self.issuance_cost if not self.external_id else xof_amount
        txn = Transaction.objects.request(**{
            'obj': self,
            'name': self.profile.name,
            'amount': total_amount,
            'phone': phone,
            'gateway': gateway,
            'initiator': self.profile.user
        })
        KashTransaction.objects.create(
            amount=txn.amount,
            sender=self.profile,
            txn_ref=txn.reference,
            txn=txn,
            timestamp=txn.created,
            profile=self.profile,
            narration="Recharge d'une carte virtuelle 💳",
            receiver=self,
            txn_type=KashTransaction.TxnType.debit,
        )
        FundingHistory.objects.create(txn_ref=txn.reference, card=self, amount=amount, status='pending')
        return txn

    def fund(self, amount, usd_amount):
        from kash.models import Wallet
        if not hasattr(self.profile, "wallet"):
            Wallet.objects.create(profile=self.profile)

        converted_amount = Money(round(amount.amount / Conversions.get_usd_rate(), 7), "USD")

        self.profile.wallet.pay(converted_amount, "Recharge de carte")
        try:
            self.fund_external(Money(usd_amount, "USD"))
        except:
            self.profile.wallet.deposit(amount)

    def fund_external(self, amount):
        if not self.external_id:
            return None

        if settings.DEBUG:
            print(f"Card funded: ${amount}")
            return

        usd_balance = rave_request("GET", "/balances/USD").json().get('data').get('available_balance')
        debit_currency = 'NGN'
        if amount.amount <= usd_balance - 5:
            debit_currency = 'USD'

        data = {
            'amount': float(amount.amount),
            'debit_currency': debit_currency
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
        withdraw_amount = Conversions.get_xof_from_usd(amount, is_withdrawal=True)
        if hasattr(self.profile, "wallet"):
            transaction = TransactionBuilder(
                source_account=StellarHelpers.get_master_account(),
                network_passphrase=settings.STELLAR_NETWORK_PASSPHRASE,
                base_fee=100000
            ).append_payment_op(
                destination=self.profile.wallet.external_id,
                amount=round(withdraw_amount.amount / Conversions.get_usd_rate(), 7),
                asset_issuer=settings.USDC_ASSET.issuer,
                asset_code=settings.USDC_ASSET.code
            ).add_text_memo(f'Retrait de la carte').build()
            transaction.sign(StellarHelpers.master_keypair)
            StellarHelpers.submit_transaction(transaction)
        else:
            payout_method = self.profile.momo_accounts.first()
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
        self.external_id = ''
        self.is_active = False
        self.save()
        return


class FundingHistory(BaseModel):
    class FundingStatus(models.TextChoices):
        success = 'success'
        failed = 'failed'
        pending = 'pending'

    txn_ref = models.CharField(max_length=255, unique=True)
    card = models.ForeignKey(VirtualCard, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=17, decimal_places=2, default_currency="XOF")
    status = models.CharField(max_length=15)


class WithdrawalHistory(BaseModel):
    txn_ref = models.CharField(max_length=255, unique=True)
    card = models.ForeignKey(VirtualCard, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=17, decimal_places=2, default_currency="XOF")


@receiver(transaction_status_changed)
def fund_card(sender, **kwargs):
    from kash.models import Notification
    txn = kwargs.pop("transaction")
    vcard_type = ContentType.objects.get_for_model(VirtualCard)

    if txn.content_type == vcard_type and txn.status == TransactionStatusEnum.failed.value:
        item = FundingHistory.objects.filter(txn_ref=txn.reference, card=txn.content_object).first()
        if item:
            item.status = FundingHistory.FundingStatus.failed
            item.save()

    if txn.content_type == vcard_type and txn.status == TransactionStatusEnum.success.value:
        card = txn.content_object
        item = FundingHistory.objects.filter(txn_ref=txn.reference, card=card).first()
        if item and item.status == FundingHistory.FundingStatus.pending:
            if card.external_id:
                card.fund_external(item.amount)
            else:
                card.create_external(item.amount)
            item.status = FundingHistory.FundingStatus.success
            item.save()
