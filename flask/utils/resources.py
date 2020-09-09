import sys
from flask import current_app as app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.exceptions import JWTExtendedException
from restless.exceptions import NotFound, RestlessError
from restless.utils import format_traceback

from restless.fl import FlaskResource

from app import db
from models import User


class ModelResource(FlaskResource):
    model: db.Model = None
    lookup_field = "id"

    def find_or_404(self, lookup_value):
        if self.lookup_field == "id":
            item = self.model.find(lookup_value)
        else:
            item = self.model.where(self.lookup_field, lookup_value).first()
        if not item:
            raise NotFound()
        return item

    def get_object(self, lookup_value):
        return self.find_or_404(lookup_value)

    def handle_error(self, err):
        if isinstance(err, RestlessError):
            data = {
                'error': err.args[0],
            }

            body = self.serializer.serialize(data)
            status = getattr(err, 'status', 500)
        elif isinstance(err, APIError):
            body = err.data
            status = err.status
        else:
            body = self.serializer.serialize({"error": "Internal Server Error"})
            status = 500

        app.logger.error(format_traceback(sys.exc_info()))
        return self.build_response(body, status=status)

    def get_collection(self):
        return self.model.all()

    def list(self, *args, **kwargs):
        return self.get_collection().serialize()

    def detail(self, pk):
        return self.get_object(pk).serialize()

    def create(self):
        item = self.model.create(**self.data)
        return self.get_object(item.get_attribute(self.lookup_field)).serialize()

    def update(self, pk):
        item = self.find_or_404(pk)
        item.update(**self.data)
        return self.get_object(item.get_attribute(self.lookup_field)).serialize()


class APIError(Exception):

    def __init__(self, status=500, data=None):
        self.status = status
        self.data = data


class AuthMixin:
    def is_authenticated(self):
        try:
            verify_jwt_in_request()
            return True
        except JWTExtendedException:
            return self.request_method() == "GET"

    @property
    def user(self):
        identity = get_jwt_identity()
        return User.find(identity.get("user_id"))
