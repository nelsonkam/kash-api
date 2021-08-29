import re
from datetime import timedelta, date
from urllib import parse

from django.conf import settings
from djmoney.money import Money

from core.utils.payment import rave_request, rave2_request
from kash.card_providers.base import BaseCardProvider


class RaveCardProvider(BaseCardProvider):
    def issue(self, card, initial_amount):
        if card.external_id:
            return

        usd_balance = rave_request("GET", "/balances/USD").json().get('data').get('available_balance')
        debit_currency = 'NGN'
        if initial_amount.amount <= usd_balance:
            debit_currency = 'USD'

        resp = rave_request('POST', '/virtual-cards', {
            'currency': 'USD',
            'amount': float(initial_amount.amount),
            'billing_name': card.profile.name,
            'debit_currency': debit_currency,
            'callback_url': "https://prod.mykash.africa/kash/virtual-cards/txn_callback/"
        }).json()

        if resp.get('data'):
            card.external_id = resp.get('data').get('id')
            masked_pan = resp.get('data').get("masked_pan")
            card.last_4 = masked_pan[len(masked_pan) - 4:len(masked_pan)]
            card.save()
        else:
            raise Exception(f"Card creation failed: {resp.get('message')}")

    def fund(self, card, amount):
        usd_balance = rave_request("GET", "/balances/USD").json().get('data').get('available_balance')
        debit_currency = 'NGN'
        if amount.amount <= usd_balance - 5:
            debit_currency = 'USD'

        data = {
            'amount': float(amount.amount),
            'debit_currency': debit_currency
        }

        return rave_request("POST", f'/virtual-cards/{card.external_id}/fund', data)

    def freeze(self, card):
        rave_request("PUT", f'/virtual-cards/{card.external_id}/status/block')

    def unfreeze(self, card):
        rave_request("PUT", f'/virtual-cards/{card.external_id}/status/unblock')

    def withdraw(self, card, amount):
        rave_request("POST", f'/virtual-cards/{card.external_id}/withdraw', {
            'amount': int(amount.amount)
        })

    def terminate(self, card):
        rave_request("PUT", f'/virtual-cards/{card.external_id}/terminate')

    def get_details(self, card):
        rave2_request("POST", f'/cardservice/balance/{card.external_id}?seckey={settings.RAVE_SECRET_KEY}')
        resp = rave_request('GET', f'/virtual-cards/{card.external_id}')
        data = resp.json().get("data")
        masked_pan = data.get("masked_pan")
        card.last_4 = masked_pan[len(masked_pan) - 4:len(masked_pan)]
        card.save()
        return data

    def get_statement(self, card):
        data = self._rave2_transactions(card) or []
        return [{**i, 'type': i.get('type').lower(), 'created_at': i.get('date'), 'status': "success", } for i in data]

    def get_transactions(self, card):
        def format_reference(ref):
            if re.match(r'^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$', ref.upper()):
                return 'Kash'
            return ref

        data = [{
            'id': item.get("id"),
            'status': item.get("status"),
            'indicator': item.get('indicator'),
            'gateway_reference_details': format_reference(item.get('gateway_reference_details')),
            'narration': item.get('narration') or item.get('product'),
            'product': item.get('product'),
            'amount': item.get('amount'),
            'fee': item.get('fee'),
            'currency': item.get('currency'),
            'created_at': item.get('created_at')
        } for item in self._rave_transactions(card)]
        return data

    def _rave2_transactions(self, card):
        data = {
            "FromDate": (card.created_at - timedelta(days=90)).date().isoformat(),
            "ToDate": (date.today() + timedelta(days=1)).isoformat(),
            "PageIndex": 0,
            "PageSize": 20,
            "CardId": card.external_id,
            "secret_key": settings.RAVE_SECRET_KEY
        }
        resp = rave2_request("POST", '/services/virtualcards/transactions', data)
        return resp.json().get("Statements")

    def _rave_transactions(self, card):
        query = {
            'from': (date.today() - timedelta(days=190)).isoformat(),
            'to': (date.today() + timedelta(days=1)),
            'size': 20,
            'index': 1
        }
        resp = rave_request('GET', f'/virtual-cards/{card.external_id}/transactions?{parse.urlencode(query)}')
        return resp.json().get('data')

    def is_balance_sufficient(self, amount):
        ngn_balance = rave_request("GET", "/balances/NGN").json().get("data").get("available_balance")
        usd_balance = rave_request("GET", "/balances/USD").json().get("data").get("available_balance")
        data = rave_request("GET", f'/rates?from=USD&to=NGN&amount={amount.amount}').json()
        ngn_amount = Money(data.get('data').get('to').get('amount'), "NGN")
        return ngn_balance >= ngn_amount.amount or usd_balance >= amount.amount
