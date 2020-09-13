import requests
import stripe
from django.conf import settings

FEDAPAY_URL = "https://sandbox-api.fedapay.com"


def fedapay_request(method, url, data=None):
    headers = {"Authorization": f"Bearer {settings.FEDAPAY_API_KEY}"}
    return requests.request(method, FEDAPAY_URL + url, json=data, headers=headers)


class Payment:
    @classmethod
    def create_transaction(cls, checkout, method="card"):
        if method == "card":
            return StripePayment.create_transaction(checkout)
        else:
            return FedaPayment.create_transaction(checkout)


class FedaPayment:
    @classmethod
    def create_transaction(cls, checkout):
        names = checkout.customer.name.split(" ")
        customer = {
            "firstname": names[0],
        }
        if len(names) > 1:
            customer["lastname"] = names[1]

        if checkout.customer.email:
            customer["email"] = checkout.customer.email

        resp = fedapay_request(
            "post",
            "/v1/transactions",
            {
                "description": "Paiement sur Kweek",
                "amount": checkout.total(),
                "callback_url": f"https://kweek.africa/order/{checkout.uid}/confirmed",
                "currency": {"iso": "XOF"},
                "customer": customer,
            },
        )
        transaction = resp.json()["v1/transaction"]
        token = cls.create_payment_token(transaction.get("id"))
        return {"payment_url": token.get("url"), "processor": "fedapay"}

    @classmethod
    def create_payment_token(cls, payment_id):
        return fedapay_request("post", f"/v1/transactions/{payment_id}/token").json()


class StripePayment:
    @classmethod
    def create_transaction(cls, checkout):
        items = [
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": item.product.name,},
                    "unit_amount": round(item.product.price / 5),
                },
                "quantity": item.quantity,
            }
            for item in checkout.cart.items.prefetch_related("product").all()
        ]
        items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "Shipping Fees", },
                "unit_amount": round(checkout.shipping_fees() / 5),
            },
            "quantity": 1,
        })
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=items,
            mode="payment",
            customer_email=checkout.customer.email,
            client_reference_id=checkout.customer.id,
            success_url=f"https://kweek.africa/order/{checkout.uid}/confirmed",
            cancel_url=f"https://kweek.africa/checkout/{checkout.uid}/shipping",
            metadata={
                'checkout_id': checkout.uid,
            }
        )

        return {"processor": "stripe", "session_id": session.id}
