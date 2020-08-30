import secrets

from orator.orm import belongs_to, has_many
from slugify import slugify
from app import db


class Product(db.Model):
    @belongs_to
    def category(self):
        from models import Category

        return Category

    @belongs_to
    def shop(self):
        from models import Shop

        return Shop

    @has_many
    def images(self):
        from models import ProductImage

        return ProductImage


class Observer(object):
    def creating(self, product):
        product.slug = slugify(product.name, max_length=40) + "-" + secrets.token_hex(2)


Product.observe(Observer())
