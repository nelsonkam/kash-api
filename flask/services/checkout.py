import json

from flask import (
    Blueprint,
    render_template,
    flash,
    url_for,
    redirect,
    abort,
    jsonify,
    request,
)
from orator import Collection

from models import Checkout, User, Customer, Cart
from utils.payment import Payment
from utils.resources import ModelResource

blueprint = Blueprint("checkout", __name__, url_prefix="/checkout")


class CheckoutResource(ModelResource):
    model = Checkout

    def get_collection(self):
        return Collection(items=[])

    def is_authenticated(self):
        return self.request_method() in ["GET", "POST"]

    def create(self):
        checkout = Checkout()
        contact: str = self.data.get("contact", "")
        if "@" in contact:
            customer = Customer.where("email", contact).first() or Customer()
            customer.email = contact
        else:
            customer = Customer.where("phone_number", contact).first() or Customer()
            customer.phone_number = contact
        customer.name = self.data.get("name", "")
        customer.save()
        checkout.customer_id = customer.id
        checkout.country = self.data.get("country")
        checkout.city = self.data.get("city")
        checkout.address = self.data.get("address")
        checkout.cart_id = Cart.where("uid", self.data.get("cart_uid")).first().id
        checkout.save()
        return self.get_object(checkout.id).serialize()


@blueprint.route("/<uid>/shipping/")
def shipping(uid):
    checkout = Checkout.where("uid", uid).first()
    if not checkout:
        return jsonify({"error": "Not Found"}), 404

    if checkout.country.lower() == "benin":
        if "cotonou" in checkout.city.lower():
            return jsonify(
                [
                    {
                        "name": "Futurix Logistic",
                        "price": {"amount": 1000, "currency": "XOF"},
                        "eta": "1-2 jours",
                    }
                ]
            )
        elif "calavi" in checkout.city.lower():
            return jsonify(
                [
                    {
                        "name": "Futurix Logistic",
                        "price": {"amount": 1500, "currency": "XOF"},
                        "eta": "1-2 jours",
                    }
                ]
            )
        else:
            return jsonify(
                [
                    {
                        "name": "Futurix Logistic",
                        "price": {"amount": 2500, "currency": "XOF"},
                        "eta": "2-3 jours",
                    }
                ]
            )
    else:
        return jsonify(
            [
                {
                    "name": "Futurix Logistic",
                    "price": {"amount": 21000, "currency": "XOF"},
                    "eta": "7-14 jours",
                }
            ]
        )


@blueprint.route("/<uid>/pay/", methods=["post"])
def pay(uid):
    checkout = Checkout.where("uid", uid).first()
    if not checkout:
        return jsonify({"error": "Not found"}), 404

    data = request.json

    if data.get("shipping"):
        checkout.shipping_option = json.dumps(data.get("shipping"))
        checkout.save()

    transaction = Payment.create_transaction(checkout)
    token = Payment.create_payment_token(transaction.get("id"))
    return {"payment_url": token.get("url")}


CheckoutResource.add_url_rules(blueprint, "/")
