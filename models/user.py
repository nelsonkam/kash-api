from app import db
from models import mixins


class User(db.Model, mixins.BaseMixin):
    username = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.Text)
    shops = db.relationship('Shop', backref='owner', lazy=True)




