from flask import Blueprint, current_app as app, jsonify, request, abort
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    jwt_optional,
    verify_jwt_in_request,
)
from flask_jwt_extended.exceptions import JWTExtendedException

from models import User, Shop
from utils.graphql import graphql
from utils.resources import ModelResource, APIError
from utils.slack import send_message
import config

blueprint = Blueprint("shop", __name__, url_prefix="/shop")


class ShopResource(ModelResource):
    lookup_field = "username"
    model = Shop

    def get_object(self, lookup_value):
        shop = super().get_object(lookup_value)
        shop.load("products")
        return shop

    def is_authenticated(self):
        try:
            verify_jwt_in_request()
            return True
        except JWTExtendedException:
            return self.request_method() == "GET"

    @property
    def user(self):
        identity = get_jwt_identity()
        return User.find(identity.get("user_id"))

    def create(self):
        print(self.data)
        if Shop.where("username", self.data.get("username")).first():
            raise APIError(
                data={
                    "errors": {
                        "username": {
                            "message": "Username already exists",
                            "code": "unique_username",
                        }
                    }
                },
                status=400,
            )

        shop = Shop()
        shop.username = self.data.get("username")
        shop.name = self.data.get("name")
        shop.phone_number = self.data.get("phone_number")
        shop.whatsapp_number = self.data.get("phone_number")
        shop.avatar_url = self.data.get("avatar_url")
        shop.user_id = self.user.id
        shop.save()
        shop.load("products")
        return shop.serialize()


ShopResource.add_url_rules(blueprint, "/")
