from orator.orm import has_many

from app import db


class Customer(db.Model):

    @has_many
    def checkouts(self):
        from models import Checkout
        return Checkout

    @has_many
    def carts(self):
        from models import Cart
        return Cart
