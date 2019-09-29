from flask import Blueprint, current_app as app, jsonify, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from utils.graphql import graphql
blueprint = Blueprint("shop", __name__, url_prefix="/shop")


@blueprint.route("/create", methods=["POST"])
def create_shop():
    data = request.get_json()

    query = """
        mutation ($shop_name: String!, $phone_number: String!, $username: String!, $description: String!, $avatar_url: String!) {
            insert_shop(objects: {name: $shop_name, username: $username, whatsapp_number: $phone_number, description: $description, avatar_url: $avatar_url}) {
                returning {
                    id
                    name
                    username
                    whatsapp_number
                    avatar_url
                    description
                }
            }
        }
    """

    resp = graphql(
        query,
        {
            "shop_name": data.get("name"),
            "phone_number": data.get("phone"),
            "username": data.get("username"),
            "avatar_url": data.get("avatar_url"),
            "description": data.get("description"),
        },
    )

    if "errors" in resp:
        error = resp.get("errors")[0]
        code = "UNKNOWN_ERROR"
        if "unique" in error.get("message"):
            if "user_id" in error.get("message"):
                code = "SHOP_EXISTS"
            elif "username" in error.get("message"):
                code = "USERNAME_TAKEN"
        return jsonify({"code": code, "message": error.get("message")}), 400

    shop = resp.get("data").get("insert_shop").get("returning")[0]

    message = [
        {
            "fallback": f"New shop created!💪🏾",
            "color": "#30BCED",
            "actions": [
                {
                    "type": "button",
                    "text": "📞 Contact on WhatsApp",
                    "url": "https://wa.me/" + shop.get("whatsapp_number")[1:],
                }
            ],
            "pretext": "New shop created!💪🏾",
            "fields": [
                {"title": "Name", "value": shop.get("name"), "short": True},
                {"title": "Username", "value": shop.get("username"), "short": True},
                {
                    "title": "Phone Number",
                    "value": shop.get("whatsapp_number"),
                    "short": True,
                },
            ],
        }
    ]
    channel = "#notifications" if config.APP_ENV == "production" else "#dev-test"
    send_message(message, channel)
    return jsonify({"shop": shop})