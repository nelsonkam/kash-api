from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    jwt_optional,
    create_refresh_token,
)
import phonenumbers
from phonenumbers import NumberParseException

import config
from models import User
from models.phone_verification import PhoneVerification
from utils.graphql import graphql
from utils.slack import send_message

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@blueprint.route("/jwt/request", methods=["POST"])
def auth_jwt():
    data = request.get_json()
    token = data.get("id_token")
    firebase_id = data.get("firebase_id")

    query = """
    query($firebase_id: String) {
      user(where: {firebase_id: {_eq: $firebase_id}}) {
        avatar_url
        id
        name
        phone_number
        username
        shops {
            id
            name
            username
            avatar_url
            whatsapp_number
        }
      }
    }
  """

    resp = graphql(query, {"firebase_id": firebase_id})

    users = resp.get("data").get("user")

    user = users[0] if len(users) > 0 else None

    try:

        return jsonify(
            {
                "access_token": create_access_token(
                    {
                        "phone_number": None,
                        "firebase_id": None,
                        "user_id": user.get("id") if user else None,
                    }
                ),
                "user": user,
            }
        )
    except Exception as err:
        print(err)
        return jsonify({"message": "User with phone number has not been verified"}), 404


@blueprint.route("/hasura/authenticate")
@jwt_optional
def hasura_auth():
    identity = get_jwt_identity()

    if identity:
        user_id = identity.get("user_id")
        return jsonify({"X-Hasura-User-Id": str(user_id), "X-Hasura-Role": "user"})
    else:
        return jsonify({"X-Hasura-Role": "anonymous"})


@blueprint.route("/account/create", methods=["POST"])
@jwt_required
def auth_create_account():
    identity = get_jwt_identity()
    data = request.get_json()

    query = """
    mutation ($name: String!, $phone_number: String!, $firebase_id: String!, $avatar_url: String!) {
        insert_user(objects: {name: $name, phone_number: $phone_number, firebase_id: $firebase_id, avatar_url: $avatar_url}) {
            returning {
                avatar_url
                id
                name
                phone_number
                username
                shops {
                    id
                    name
                    username
                    whatsapp_number
                    avatar_url
                    description
                }
            }
        }
    }
    """

    resp = graphql(
        query,
        {
            "name": data.get("name"),
            "avatar_url": data.get("avatar_url"),
            "phone_number": identity.get("phone_number"),
            "firebase_id": identity.get("firebase_id"),
        },
    )

    if "errors" in resp:
        error = resp.get("errors")[0]
        code = "UNKNOWN_ERROR"
        if "unique" in error.get("message"):
            code = "USER_EXISTS"
        return jsonify({"code": code, "message": error.get("message")}), 400

    user = resp.get("data").get("insert_user").get("returning")[0]

    message = [
        {
            "fallback": f"New account created!💪🏾",
            "actions": [
                {
                    "type": "button",
                    "text": "📞 Contact on WhatsApp",
                    "url": "https://wa.me/" + user.get("phone_number")[1:],
                }
            ],
            "color": "#30BCED",
            "pretext": "New account created!💪🏾",
            "fields": [
                {"title": "Name", "value": user.get("name"), "short": True},
                {"title": "Username", "value": user.get("username"), "short": True},
                {
                    "title": "Phone Number",
                    "value": user.get("phone_number"),
                    "short": True,
                },
            ],
        }
    ]
    channel = "#notifications" if config.APP_ENV == "production" else "#dev-test"
    send_message(message, channel)
    return jsonify(
        {
            "user": user,
            "access_token": create_access_token(
                {
                    "phone_number": identity.get("phone_number"),
                    "firebase_id": identity.get("firebase_id"),
                    "user_id": user.get("id"),
                }
            ),
        }
    )


@blueprint.route("/shop/create", methods=["POST"])
@jwt_required
def create_shop():
    identity = get_jwt_identity()
    data = request.get_json()

    query = """
        mutation ($shop_name: String!, $phone_number: String!, $username: String!, $description: String!, $avatar_url: String!, $user_id: uuid!) {
            insert_shop(objects: {name: $shop_name, username: $username, whatsapp_number: $phone_number, user_id: $user_id, description: $description, avatar_url: $avatar_url}) {
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
            "shop_name": data.get("shop_name"),
            "phone_number": data.get("shop_phone"),
            "username": data.get("username"),
            "user_id": data.get("user_id"),
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


@blueprint.route("/shop/current")
@jwt_required
def get_shop():
    identity = get_jwt_identity()

    query = """
    query ($id: uuid!) {
        shop(where: {user_id: {_eq: $id}}) {
            id
            description
            name
            products {
            id
            name
            price
            sold
            product_images {
                id
                url
            }
            
            }
            avatar_url
            username
            whatsapp_number
        }
    }
    """

    resp = graphql(query, {"id": identity.get("user_id")})

    if "errors" in resp:
        error = resp.get("errors")[0]
        code = "UNKNOWN_ERROR"
        return jsonify({"code": code, "message": error.get("message")}), 400

    shop = resp.get("data").get("shop")[0]

    return jsonify({"shop": shop})


@blueprint.route("/phone/register", methods=["POST"])
def phone_register():
    phone_number = request.json.get("phone_number")
    try:
        number = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(number):
            return jsonify({"error": "Invalid phone number"}), 400
    except NumberParseException:
        return jsonify({"error": "Invalid phone number"}), 400

    verification = PhoneVerification.send_verification_code(phone_number)

    return jsonify({"session_token": verification.session_token})


@blueprint.route("/phone/verify", methods=["POST"])
def phone_verify():
    session_token = request.json.get("session_token")
    security_code = request.json.get("security_code")
    phone_number = request.json.get("phone_number")
    if PhoneVerification.verify(phone_number, security_code, session_token):
        user = User.where("phone_number", phone_number).first() or User()
        user.phone_number = phone_number
        user.save()
        user.load("shops")
        return jsonify(
            {
                "access": create_access_token(
                    {"phone_number": phone_number, "user_id": user.id,}
                ),
                "refresh": create_refresh_token(
                    {"phone_number": phone_number, "user_id": user.id,}
                ),
                "user": user.serialize()
            }
        )
    return jsonify({"error": "Invalid verification credentials"}), 400
