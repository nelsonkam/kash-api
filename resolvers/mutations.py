from ariadne import MutationType

from app import db
from models import Cart, Item

mutation = MutationType()

@mutation.field("add_to_cart")
def resolve_add_to_cart(_, info, product_id, quantity, cart_id=None):
    cart = Cart()
    if cart_id:
        cart = Cart.find_or_fail(cart_id)
    item = Item(product_id=product_id, quantity=quantity)
    item.total = item.compute_total()
    cart.items.append(item)
    db.session.add(cart)
    db.session.add(item)
    return cart

@mutation.field("delete_cart_item")
def resolve_delete_cart_item(_, info, id):
    item = Item.find_or_fail(id)
    item.delete()
    return id

@mutation.field("update_cart_item")
def resolve_update_cart_item(_, info, id, quantity):
    item = Item.find_or_fail(id)
    item.quantity = quantity
    item.save()
    return item
