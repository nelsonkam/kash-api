from orator.orm import has_many

from app import db


class Category(db.Model):
    @has_many
    def products(self):
        from models import Product

        return Product
