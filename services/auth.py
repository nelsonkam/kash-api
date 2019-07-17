from flask import Blueprint, current_app as app, jsonify, request, abort
from firebase_admin import auth
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required
from utils import firebase
from utils.graphql import client
import config
import requests
import json

blueprint = Blueprint('auth', __name__, url_prefix="/auth")


@blueprint.route('/jwt/request', methods=["POST"])
def auth_jwt():
  data = request.get_json()
  token = data.get('id_token')
  firebase_id = data.get('firebase_id')

  query = """
    query($firebase_id: String) {
      users(where: {firebase_id: {_eq: $firebase_id}) {
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

  resp = client.execute(query, variables={'firebase_id': firebase_id})

  users = json.load(resp).get("data").get("users")
  user = users[0] if len(users) > 0 else None
  
  try:
    firebase_user = auth.verify_id_token(token)
    
    return jsonify({
      "access_token": create_access_token({
        "phone_number": firebase_user["phone_number"], 
        "firebase_id": firebase_user["uid"],
        "user_id": user.get("id") if user else None
      }),
      "user": user
    })
  except Exception as err:
    print(err)
    return jsonify({"message": "User with phone number has not been verified"}), 404

@blueprint.route("/account/create", methods=["POST"])
@jwt_required
def auth_create_account():
  identity = get_jwt_identity()
  data = request.get_json()

  query = """
    mutation($avatar_url: String!, $name: String!, $phone_number: String!, $username: String!, $firebase_id: String!) {
      insert_users(objects: {avatar_url: $avatar_url, name: $name, phone_number: $phone_number, username: $username, firebase_id: $firebase_id}) {
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

  resp = client.execute(query, variables={
    'avatar_url': data.get("avatar_url"),
    'name': data.get("name"),
    'phone_number': identity.get("phone_number"),
    'username': data.get("username"),
    'firebase_id': identity.get("firebase_id"),
  })

  resp = json.load(resp)

  if "errors" in resp:
    error = resp.get("errors")[0]
    code = 'UNKNOWN_ERROR'
    if 'username_unique' in error.get("message"):
      code = 'USERNAME_TAKEN' 
    elif 'firebase_id_unique' in error.get("message"):
      code  = 'USER_EXISTS'
    return jsonify({'code': code}), 400


  user = resp.get("data").get('insert_users').get("returning")[0]

  return jsonify({
    'data': user, 
    "access_token": create_access_token({
      "phone_number": identity.get("phone_number"), 
      "firebase_id": identity.get("firebase_id"),
      "user_id": user.get("id")
    })
  })
