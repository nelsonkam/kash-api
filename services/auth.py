from flask import Blueprint, current_app as app, jsonify, request, abort
from firebase_admin import auth
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from utils import firebase
from utils.slack import send_message
import config
import requests

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


def graphql(query, variables):
    headers = {"x-hasura-admin-secret": config.GQL_ENGINE_SECRET}
    json = {"query": query, "variables": variables}

    resp = requests.post(config.GQL_ENGINE_URL, json=json, headers=headers)
    return resp.json()


@blueprint.route("/jwt/request", methods=["POST"])
def auth_jwt():
    data = request.get_json()
    token = data.get("id_token")
    firebase_id = data.get("firebase_id")

    query = """
    query($firebase_id: String) {
      user(where: {firebase_id: {_eq: $firebase_id}}) {
        avatar_url
        created_at
        id
        name
        phone_number
        username
        updated_at
      }
    }
  """

    headers = {"x-hasura-admin-secret": config.GQL_ENGINE_URL}

    resp = graphql(query, {"firebase_id": firebase_id})

    users = resp.get("data").get("user")

    user = users[0] if len(users) > 0 else None

    try:
        firebase_user = auth.verify_id_token(token)

        return jsonify(
            {
                "access_token": create_access_token(
                    {
                        "phone_number": firebase_user["phone_number"],
                        "firebase_id": firebase_user["uid"],
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
@jwt_required
def hasura_auth():
    identity = get_jwt_identity()
    user_id = identity.get("user_id")
    if user_id:
        return jsonify({"X-Hasura-User-Id": str(user_id), "X-Hasura-Role": "user"})
    else:
        abort(401)


@blueprint.route("/account/create", methods=["POST"])
@jwt_required
def auth_create_account():
    identity = get_jwt_identity()
    data = request.get_json()

    query = """
    mutation ($name: String!, $phone_number: String!, $firebase_id: String!) {
        insert_user(objects: {name: $name, phone_number: $phone_number, firebase_id: $firebase_id}) {
            returning {
            id
            avatar_url
            name
            username
            phone_number
            }
        }
    }
    """

    resp = graphql(
        query,
        {
            "name": data.get("name"),
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

    query = """
    mutation ($shop_name: String!, $phone_number: String!, $username: String!, $user_id: uuid!) {
      insert_shop(objects: {name: $shop_name, username: $username, whatsapp_number: $phone_number, user_id: $user_id}) {
        returning {
          id
          name
          username
          whatsapp_number
        }
      }
    }
  """

    resp = graphql(
        query,
        {
            "shop_name": data.get("shopName"),
            "phone_number": data.get("shopPhone"),
            "username": data.get("username"),
            "user_id": user.get("id"),
        },
    )

    if "errors" in resp:
        error = resp.get("errors")[0]
        code = "UNKNOWN_ERROR"
        if "username_unique" in error.get("message"):
            code = "USERNAME_TAKEN"
        return jsonify({"code": code, "message": error.get("message")}), 400

    shop = resp.get("data").get("insert_shop").get("returning")[0]

    message = [
        {
            "fallback": f"New account created!💪🏾",
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
            "shop": shop,
            "access_token": create_access_token(
                {
                    "phone_number": identity.get("phone_number"),
                    "firebase_id": identity.get("firebase_id"),
                    "user_id": user.get("id"),
                }
            ),
        }
    )
