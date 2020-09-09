from orator.orm import has_many

from app import db


class User(db.Model):

    @has_many
    def shops(self):
        from models import Shop

        return Shop




