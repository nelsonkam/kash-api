from flask import Blueprint, current_app as app, jsonify, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from utils.upload import save_file, allowed_file

blueprint = Blueprint('upload', __name__, url_prefix="/upload")

@blueprint.route('/', methods=['POST'])
@jwt_required
def upload():
  image = request.files.get('image')
  if image and allowed_file(image.filename):
    url = save_file(image)
    return jsonify({'url': url})
  else:
    return jsonify({'error': '400 Bad Request'}), 400