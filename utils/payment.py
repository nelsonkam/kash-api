import requests
import config

FEDAPAY_URL = "https://sandbox-api.fedapay.com"

def fedapay_request(method, url, data=None):
    headers = {
        "Authorization": f"Bearer {config.FEDAPAY_API_KEY}"
    }
    return requests.request(method, FEDAPAY_URL + url, json=data, headers=headers)

class Payment:
    @classmethod
    def create_transaction(cls, checkout):
        names = checkout.customer.name.split(" ")
        customer = {
            "firstname": names[0],
        }
        if len(names) > 1:
            customer.lastname = names[1]

        if checkout.customer.email:
            customer['email'] = checkout.customer.email

        resp = fedapay_request("post", "/v1/transactions", {
            "description": "Paiement sur Kweek",
            "amount": checkout.total(),
            "callback_url": "https://kweek.africa/order/confirmed",
            "currency": {"iso": "XOF"},
            "customer": customer
        })
        return resp.json()['v1/transaction']


    @classmethod
    def create_payment_token(cls, payment_id):
        return fedapay_request('post', f'/v1/transactions/{payment_id}/token').json()
