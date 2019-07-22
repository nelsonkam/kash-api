from flask import Blueprint, current_app as app, jsonify, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from utils.slack import send_message
import config

blueprint = Blueprint('nofify', __name__, url_prefix="/nofify")

@blueprint.route('/feedback', methods=['POST'])
@jwt_required
def send_feedback():
  data = request.get_json()
  user = data.get("user")
  feedback = data.get("message")
  if user and feedback:
    message = [
      {
        "fallback": f"Feedback from @{user.get('username')}: {feedback}",
        "actions": [
          {
            "type": "button",
            "text": "📞 Contact on WhatsApp",
            "url": "https://wa.me/"+user.get("phone_number")[1:]
          }
        ],
        "color": "#30BCED",
        "pretext": "You've got new feedback.",
        "text": "",
        "fields": [
          {
            "title": "Name",
            "value": user.get("name"),
            "short": True
          },
          {
            "title": "WhatsApp",
            "value": user.get("phone_number"),
            "short": True
          },
          {
            "title": "Feed",
            "value": feedback,
            "short": False
          }
        ],
      }
    ]
    channel = "#customer-research" if config.APP_ENV == "production" else "#dev-test"
    return send_message(message, channel)
  else:
    return jsonify({'error': '400 Bad Request'}), 400