import requests
import stripe
from django.conf import settings
from kkiapay import Kkiapay

FEDAPAY_URL = (
    "https://sandbox-api.fedapay.com" if settings.DEBUG else "https://api.fedapay.com"
)


def fedapay_request(method, url, data=None):
    headers = {"Authorization": f"Bearer {settings.FEDAPAY_API_KEY}"}
    return requests.request(method, FEDAPAY_URL + url, json=data, headers=headers)


class Payment:
    @classmethod
    def get_processor_cls(cls, method):
        return {"card": StripePayment, "cash": CashOnDelivery, "momo": KKiaPayment}[
            method
        ]

    @classmethod
    def create_transaction(cls, checkout, method="card", **kwargs):
        if method == "card":
            try:
                return StripePayment.create_transaction(checkout, **kwargs)
            except Exception as e:
                print("[stripe error]", e)
                return None
        elif method == "momo":
            return KKiaPayment.create_transaction(checkout, **kwargs)
        elif method == "cash":
            return CashOnDelivery.create_transaction(checkout, **kwargs)
        else:
            raise NotImplemented

    @classmethod
    def verify_transaction(cls, method="card", **kwargs):
        ProcessorClass = cls.get_processor_cls(method)

        return ProcessorClass.verify_transaction(**kwargs)


class KKiaPayment:
    @classmethod
    def create_transaction(cls, checkout, **kwargs):
        return {"processor": "kkiapay", "amount": checkout.total()}

    @classmethod
    def verify_transaction(cls, transaction_id=None, **kwargs):
        k = Kkiapay(
            settings.KKIAPAY_PUBLIC_KEY,
            settings.KKIAPAY_PRIVATE_KEY,
            settings.KKIAPAY_SECRET_KEY,
            sandbox=settings.DEBUG,
        )
        transaction = k.verify_transaction(transaction_id)
        return transaction.status == "SUCCESS"


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
        shipping_price = checkout.shipping_option.get("price")
        items.append(
            {
                "price_data": {
                    "currency": shipping_price.get("currency"),
                    "product_data": {"name": "Frais de livraison"},
                    "unit_amount": round(
                        checkout.shipping_fees()
                        if shipping_price.get("currency").lower() == "xof"
                        else checkout.shipping_fees() * 100
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
