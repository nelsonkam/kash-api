from flask import Blueprint, current_app as app, jsonify, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional

from models import Category
from utils.graphql import graphql
from utils.resources import ModelResource

blueprint = Blueprint("category", __name__, url_prefix="/category")


class CategoryResource(ModelResource):
    model = Category


CategoryResource.add_url_rules(blueprint, rule_prefix="/")


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
        categories: category(order_by: {products_aggregate: {count: desc}}) {
            id
            name
            slug
            products(order_by: {id: asc}, limit: 1, offset: 10) {
              product_images {
                url
              }
            }
          }
    }
    """
    resp = graphql(query, {"slug": slug})

    if "errors" in resp:
        error = resp.get("errors")[0]
        code = "GRAPHQL_ERROR"
        print(resp)
        return jsonify({"code": code, "message": error.get("message")}), 400

    return jsonify(resp.get("data"))
