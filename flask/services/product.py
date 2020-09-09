from flask import Blueprint, current_app as app, jsonify, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional

from models import Product
from utils.graphql import graphql
import random

from utils.resources import ModelResource, AuthMixin

blueprint = Blueprint("product", __name__, url_prefix="/product")


class ProductResource(ModelResource, AuthMixin):

    def list(self, *args, **kwargs):
        return Product.with_("images").get().serialize()

ProductResource.add_url_rules(blueprint, "/")
