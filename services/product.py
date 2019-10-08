from flask import Blueprint, current_app as app, jsonify, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from utils.graphql import graphql
import random

blueprint = Blueprint("product", __name__, url_prefix="/product")


@blueprint.route("/create", methods=["POST"])
@jwt_optional
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


@blueprint.route("/similar/<product_id>")
def similar(product_id):
    query = """
    query ($id: uuid!){
        product(where: {id: {_eq: $id}}) {
            category {
                products {
                    description
                    created_at
                    id
                    name
                    price
                    product_images {
                        id
                        url
                        created_at
                    }
                }
            }
        }
    }
    """
    resp = graphql(query, {"id": product_id})

    if "errors" in resp:
        code = "GRAPHQL_ERROR"
        return jsonify({"code": code, "message": error.get("message")}), 400

    product = resp.get("data").get("product")[0]

    if not product:
        code = "PRODUCT_NOT_FOUND_ERROR"
        return jsonify({"code": code, "message": "Product not found"}), 404
    elif not product.get("category"):
        code = "NO_CATEGORY_ERROR"
        return (
            jsonify({"code": code, "message": "Product doesn't have a category"}),
            404,
        )

    products = product.get("category").get("products")
    random.shuffle(products)

    return jsonify({"products": products[:2]})


@blueprint.route("/<product_id>")
def get_product(product_id):
    query = """
    query ($id: uuid!){
        product(where: {id: {_eq: $id}}) {
            id
            description
            name
            price
            product_images {
                id
                url
            }
            shop {
                id
                name
                username
                whatsapp_number
                avatar_url
            }
            category {
                products {
                    description
                    created_at
                    id
                    name
                    price
                    product_images {
                        id
                        url
                        created_at
                    }
                }
            }
        }
    }
    """
    resp = graphql(query, {"id": product_id})

    if "errors" in resp:
        code = "GRAPHQL_ERROR"
        return jsonify({"code": code, "message": error.get("message")}), 400

    product = resp.get("data").get("product")[0]
    similar_products = []
    if not product:
        code = "PRODUCT_NOT_FOUND_ERROR"
        return jsonify({"code": code, "message": "Product not found"}), 404
    elif product.get("category"):
        similar_products = product.get("category").get("products")
        random.shuffle(similar_products)
   
    

    return jsonify({"similar": similar_products[:2], "product": product})