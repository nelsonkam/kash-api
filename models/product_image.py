from app import db
from models import mixins


class ProductImage(db.Model, mixins.BaseMixin):
    url = db.Column(db.Text, nullable=False)
    product_id =  mixins.foreign_key("product")
