from flask import Blueprint, current_app as app, jsonify, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from utils.graphql import graphql

blueprint = Blueprint("product", __name__, url_prefix="/product")


@blueprint.route("/create", methods=["POST"])
@jwt_required
def create():
    data = request.get_json()
    query = """
    mutation($name: String!, $price: String!, $description: String!, $shop_id: uuid!) {
        insert_product(objects: {name: $name, price: $price, description: $description, shop_id: $shop_id}) {
            returning {
                id
                name
                price
                description
            }
        }
    }
    """

    resp = graphql(
        query,
        {
            "name": data.get("name"),
            "price": data.get("price"),
            "description": data.get("description"),
            "shop_id": data.get("shop_id"),
        },
    )

    if "errors" in resp:
        error = resp.get("errors")[0]
        code = "CREATE_PRODUCT_ERROR"
        return jsonify({"code": code, "message": error.get("message")}), 400

    product = resp.get("data").get("insert_product").get("returning")[0]

    query = """
    mutation($url: String!, $product_id: uuid!) {
        insert_product_image(objects: {url: $url, product_id: $product_id}) {
            returning {
                id
                url
            }
        }
    }
    """

    resp = graphql(
        query, {"url": data.get("image_url"), "product_id": product.get("id")}
    )

    if "errors" in resp:
        error = resp.get("errors")[0]
        code = "CREATE_PRODUCT_IMAGE_ERROR"
        return jsonify({"code": code, "message": error.get("message")}), 400

    return jsonify({"product": product})
