import requests
import stripe
from django.conf import settings

FEDAPAY_URL = (
    "https://sandbox-api.fedapay.com" if settings.DEBUG else "https://api.fedapay.com"
)

RAVE_URL = "https://api.flutterwave.com/v3"

RAVE_PAYMENT_METHODS = [
    "account", "card", "banktransfer", "mpesa", "mobilemoneyrwanda", "mobilemoneyzambia", "qr", "mobilemoneyuganda",
    "ussd", "credit", "barter", "mobilemoneyghana", "payattitude", "mobilemoneyfranco", "paga", "1voucher",
    "mobilemoneytanzania"
]


def fedapay_request(method, url, data=None):
    headers = {"Authorization": f"Bearer {settings.FEDAPAY_API_KEY}"}
    return requests.request(method, FEDAPAY_URL + url, json=data, headers=headers)


def rave_request(method, url, data=None):
    headers = {"Authorization": f"Bearer {settings.RAVE_SECRET_KEY}"}
    resp = requests.request(method, RAVE_URL + url, json=data, headers=headers)
    if 200 > resp.status_code or resp.status_code >= 399:
        if resp.json():
            raise Exception(resp.json().get('message'))
        else:
            raise Exception(f"Rave API call `{method} {url}` failed: `{resp.text}`")
    return resp



def rave2_request(method, url, data=None):
    base_url = "https://api.ravepay.co/v2"
    return requests.request(method, base_url + url, json=data)


class Payment:
    @classmethod
    def get_processor_cls(cls, method):
        return {"card": StripePayment, "cash": CashOnDelivery, "momo": KKiaPayment}[
            method
        ]

    @classmethod
    def create_transaction(cls, checkout, method="card", **kwargs):
        ProcessorClass = cls.get_processor_cls(method)
        return ProcessorClass.create_transaction(checkout)

    @classmethod
    def verify_transaction(cls, method="card", **kwargs):
        ProcessorClass = cls.get_processor_cls(method)
        return ProcessorClass.verify_transaction(**kwargs)


class KKiaPayment:
    @classmethod
    def create_transaction(cls, checkout, **kwargs):
        return {"processor": "kkiapay", "amount": checkout.total.amount}

    @classmethod
    def verify_transaction(cls, transaction_id=None, **kwargs):
        # k = Kkiapay(
        #     settings.KKIAPAY_PUBLIC_KEY,
        #     settings.KKIAPAY_PRIVATE_KEY,
        #     settings.KKIAPAY_SECRET_KEY,
        #     sandbox=settings.DEBUG,
        # )
        # transaction = k.verify_transaction(transaction_id)
        # return transaction.status == "SUCCESS"
        pass


class RavePayment:

    @classmethod
    def create_transaction(cls, checkout, **kwargs):
        shop = checkout.cart.shop
        data = {
            "tx_ref": f"TX-{checkout.ref_id}",
            "amount": checkout.total.amount,
            "currency": str(checkout.total.currency),
            "redirect_url": f"{kwargs.get('origin')}/order/{checkout.uid}/confirmed/",
            "payment_options": ",".join(RAVE_PAYMENT_METHODS),
            "meta": {
                "checkout_ref": checkout.ref_id,
            },
            "customer": {
                "email": "kamganelson@gmail.com",
                "phonenumber": checkout.customer.phone_number,
                "name": checkout.customer.name
            },
            "subaccounts": [{
                "id": shop.bankaccount.rave_subaccount_id
            }],
            "customizations": {
                "title": f"Pay {shop.name} for your order",
                # "description": "Pay",
                "logo": shop.avatar_url
            }
        }
        resp = rave_request("POST", "/payments", data)
        print(resp.text, resp.status_code)
        return {"processor": "flutterwave", "link": resp.json().get('data').get('link')}

    @classmethod
    def verify_transaction(cls, transaction_id=None, **kwargs):
        resp = rave_request("POST", f"/transactions/{transaction_id}/verify")
        return resp.json().get("data").get("status") == "successful"


class StripePayment:
    @classmethod
    def create_transaction(cls, checkout, **kwargs):
        items = [
            {
                "price_data": {
                    "currency": item.product.currency_iso,
                    "product_data": {"name": item.product.name},
                    "unit_amount": round(
                        item.product.price
                        if item.product.currency_iso.lower() == "xof"
                        else item.product.price * 100
                    ),
                },
                "quantity": item.quantity,
            }
            for item in checkout.cart.items.prefetch_related(
                "product", "product__images"
            ).all()
        ]
        items.append(
            {
                "price_data": {
                    "currency": checkout.shipping_fees.currency,
                    "product_data": {"name": "Frais de livraison"},
                    "unit_amount": round(
                        checkout.shipping_fees.amount
                        if str(checkout.shipping_fees.currency).lower() == "xof"
                        else checkout.shipping_fees.amount * 100
                    ),
                },
                "quantity": 1,
            }
        )
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=items,
            mode="payment",
            customer_email=checkout.customer.email,
            client_reference_id=checkout.customer.id,
            success_url=f"{kwargs.get('origin')}/order/{checkout.uid}/confirmed/?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=kwargs.get("return_url"),
            metadata={"checkout_id": checkout.uid},
        )

        return {"processor": "stripe", "session_id": session.id}

    @classmethod
    def verify_transaction(cls, session_id=None, **kwargs):
        session = stripe.checkout.Session.retrieve(session_id)
        return session.payment_status == "paid"


class CashOnDelivery:
    @classmethod
    def create_transaction(cls, checkout, **kwargs):
        return {"processor": "cash"}

    @classmethod
    def verify_transaction(cls, **kwargs):
        return True
