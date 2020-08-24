from app import db
from models import mixins


class Shop(db.Model, mixins.BaseMixin):
    username = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    whatsapp_number = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.Text)
    description = db.Column(db.Text)
    user_id = mixins.foreign_key("user")
    products = db.relationship("Product", backref='shop')
