import json
import secrets

from orator.orm import belongs_to

from app import db


class Checkout(db.Model):

    @belongs_to
    def cart(self):
        from models import Cart
        return Cart

    @belongs_to
    def customer(self):
        from models import Customer

        return Customer

    def total(self):
        if hasattr(self, 'shipping_option'):
            option = json.loads(self.shipping_option)
            return self.cart.total() + option.get("price").get("amount")
        return self.cart.total()

class CheckoutObserver(object):
    def creating(self, cart):
        cart.uid = secrets.token_urlsafe(10)


Checkout.observe(CheckoutObserver())
