import secrets

from orator.orm import has_many, belongs_to, has_one
from satchless.cart import Cart as SatchCart, CartLine

from app import db


class Cart(db.Model):
    @has_many
    def items(self):
        return CartItem

    def total(self):
        return sum([item.total() for item in self.items().with_("product").get()])


class CartItem(db.Model):
    @belongs_to
    def cart(self):
        return Cart

    @belongs_to
    def product(self):
        from models import Product

        return Product

    def total(self):
        return self.product.price * self.quantity

    def serialize(self):
        data = super().serialize()
        data['total'] = self.total()
        return data


class CartObserver(object):
    def creating(self, cart):
        cart.uid = secrets.token_urlsafe(10)


Cart.observe(CartObserver())
