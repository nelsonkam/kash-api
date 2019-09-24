from flask import Blueprint, current_app as app, jsonify, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from utils.graphql import graphql

blueprint = Blueprint("feed", __name__, url_prefix="/feed")

FEED_QUERY = """
{
  category(order_by: {products_aggregate: {count: desc}}) {
    id
    name
    slug
    products(limit: 1) {
      product_images {
        url
      }
    }
  }
  product(order_by: {id: asc}) {
    id
    name
    price
    sold
    product_images {
      id
      url
    }
    shop {
      id
      username
      name
      avatar_url
    }
  }
}
"""


@blueprint.route("")
def feed():
    resp = graphql(FEED_QUERY)

    if "errors" in resp:
        code = "GRAPHQL_ERROR"
        return jsonify({"code": code, "message": error.get("message")}), 400

    return jsonify(resp.get("data"))
