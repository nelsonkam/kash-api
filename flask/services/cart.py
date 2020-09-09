from flask import Blueprint
from orator import Collection

from models import Cart, CartItem
from utils.resources import ModelResource

blueprint = Blueprint("cart", __name__, url_prefix="/cart")


class CartResource(ModelResource):
    model = Cart
    lookup_field = "uid"

    def is_authenticated(self):
        return True

    def get_object(self, lookup_value):
        cart = self.find_or_404(lookup_value)
        cart.load("items", "items.product", "items.product.images")
        return cart

    def get_collection(self):
        return Collection(items=[])

    def save_items(self, cart):
        for item in self.data.get("items", []):
            cart_item = CartItem.find_or_new(item.get("id", 0))

            if item.get("id", None) and item.get("quantity", 0) == 0:
                cart_item.delete()
            else:
                cart_item.quantity = item.get("quantity")
                cart_item.product_id = item.get("product_id")
                cart_item.cart_id = cart.id
                cart_item.save()

    def create(self):
        cart = Cart()
        cart.save()
        self.save_items(cart)
        return self.get_object(cart.uid).serialize()

    def update(self, pk):
        cart = self.get_object(pk)
        self.save_items(cart)
        return self.get_object(pk).serialize()


CartResource.add_url_rules(blueprint, "/")
