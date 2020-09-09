from orator.orm import belongs_to

from app import db


class ProductImage(db.Model):
    @belongs_to
    def product(self):
        from models import Product

        return Product
