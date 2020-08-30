from restless.exceptions import NotFound
from restless.fl import FlaskResource

from app import db
from restless.fl import FlaskResource

from app import db


class ModelResource(FlaskResource):
    model: db.Model = None


    def find_or_404(self, pk):
        item = self.model.find(pk)
        if not item:
            raise NotFound()
        return item

    def list(self, *args, **kwargs):
        return self.model.all().serialize()

    def detail(self, pk):
        return self.find_or_404(pk).serialize()

    def create(self):
        return self.model.create(**self.data).serialize()

    def update(self, pk):
        item = self.find_or_404(pk)
        item.update(**self.data)
        return item.serialize()

    def delete(self, pk):
        item = self.find_or_404(pk)
        return item.delete()
