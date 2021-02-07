import requests
import stripe
from django.conf import settings
from kkiapay import Kkiapay
FEDAPAY_URL = "https://sandbox-api.fedapay.com" if settings.DEBUG else "https://api.fedapay.com"


def fedapay_request(method, url, data=None):
    headers = {"Authorization": f"Bearer {settings.FEDAPAY_API_KEY}"}
    return requests.request(method, FEDAPAY_URL + url, json=data, headers=headers)


class Payment:
    @classmethod
    def create_transaction(cls, checkout, method="card"):
        if method == "card":
            return StripePayment.create_transaction(checkout)
        else:
            return KKiaPayment.create_transaction(checkout)

    @classmethod
    def verify_transaction(cls, **kwargs):
        transaction_id = kwargs.pop("transaction_id", None)
        if transaction_id:
            return KKiaPayment.verify_transaction(transaction_id)

        session_id = kwargs.pop("session_id", None)
        if session_id:
            return StripePayment.verify_transaction(session_id)

        return False


class KKiaPayment:

    @classmethod
    def create_transaction(cls, checkout):
        return {"processor": "kkiapay", "amount": checkout.total()}

    @classmethod
    def verify_transaction(cls, transaction_id):
        k = Kkiapay(settings.KKIAPAY_PUBLIC_KEY, settings.KKIAPAY_PRIVATE_KEY, settings.KKIAPAY_SECRET_KEY, sandbox=settings.DEBUG)
        transaction = k.verify_transaction(transaction_id)
        return transaction.status == 'SUCCESS'



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
                    "product_data": {"name": item.product_details.name, },
                    "unit_amount": round(item.product_details.price / 5),
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
            success_url=f"https://kweek.africa/order/{checkout.uid}/confirmed/?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"https://kweek.africa/checkout/{checkout.uid}/shipping",
            metadata={
                'checkout_id': checkout.uid,
            }
        )

        return {"processor": "stripe", "session_id": session.id}

    @classmethod
    def verify_transaction(cls, session_id):
        session = stripe.checkout.Session.retrieve(session_id)
        return session.payment_status == 'paid'
