import sys

from restless.exceptions import NotFound, RestlessError
from restless.fl import FlaskResource
from restless.utils import format_traceback

from app import db
from restless.fl import FlaskResource

from app import db


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
        else:
            body = self.serializer.serialize({"error": "Internal Server Error"})
            status = 500


        print(format_traceback(sys.exc_info()))
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
