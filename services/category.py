from flask import Blueprint, current_app as app, jsonify, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from utils.graphql import graphql

blueprint = Blueprint("category", __name__, url_prefix="/category")


@blueprint.route("/products/<slug>")
def products(slug):
    query = """
    query ($slug: String!){
        category(where: {slug: {_eq: $slug}}) {
            name
            products {
                id
                name
                price
                product_images {
                id
                url
                }
            }
        }
    }
    """
    resp = graphql(query, {"slug": slug})

    if "errors" in resp:
        code = "GRAPHQL_ERROR"
        return jsonify({"code": code, "message": error.get("message")}), 400

    return jsonify(resp.get("data").get("category")[0])
