from orator.orm import belongs_to, has_many
from app import db

class Shop(db.Model):

    @belongs_to('user_id')
    def owner(self):
        from models import User

        return User

    @has_many
    def products(self):
        from models import Product

        return Product
