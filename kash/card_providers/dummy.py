import secrets
import string
import time

from djmoney.money import Money

from kash.card_providers.base import BaseCardProvider

BALANCE = 100


def set_dummy_balance(num):
    global BALANCE
    BALANCE = num


class DummyCardProvider(BaseCardProvider):

    def issue(self, card, initial_amount):
        if "fail" in card.nickname.lower() or initial_amount.amount < 5 or not self.is_balance_sufficient(
                initial_amount):
            raise Exception("Couldn't create card")
        time.sleep(1)
        card.external_id = secrets.token_urlsafe(20)
        card.last_4 = "".join(secrets.choice(string.digits) for i in range(4))
        card.save(update_fields=['last_4', 'external_id'])
        print(f"Card issued: {initial_amount}")
        return {
            'debit_currency': 'USD',
        }

    def fund(self, card, amount):
        if "fail" in card.nickname.lower() or amount.amount < 5 or not self.is_balance_sufficient(amount):
            raise Exception("Couldn't fund card")
        time.sleep(1)
        print(f"Card funded: {amount}")
        return {
            'debit_currency': 'USD',
        }

    def freeze(self, card):
        print("Card frozen")

    def unfreeze(self, card):
        print("Card unfrozen")

    def withdraw(self, card, amount):
        if "fail" in card.nickname.lower():
            raise Exception("Couldn't withdraw from card")
        print(f"Card withdrawn: ${amount}")

    def terminate(self, card):
        print("Card terminated.")

    def get_details(self, card):
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

    def get_transactions(self, card):
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

    def get_statement(self, card):
        data = [{
            "date": "2021-05-09",
            "amount": "150.00",
            "type": "Debit",
            "balance_before": "30.00",
            "balance_after": "180.00",
            "merchant": "Funding"
        }, {
            "date": "2021-05-08",
            "amount": "150.00",
            "type": "Credit",
            "balance_before": "30.00",
            "balance_after": "180.00",
            "merchant": "Funding"
        }]

        return [{**i, 'type': i.get('type').lower(), 'created_at': i.get('date'), 'status': "success", } for i in data]

    def is_balance_sufficient(self, amount):
        return BALANCE >= amount.amount
