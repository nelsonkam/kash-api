from app import db
from models import mixins


class Product(mixins.BaseModel):
    name = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    currency_iso = db.Column(db.String(10), nullable=False, default="XOF")
    description = db.Column(db.Text)
    shop_id = mixins.foreign_key("shop")
    category_id = mixins.foreign_key("category", nullable=True)
    images = db.relationship("ProductImage", backref="product")

