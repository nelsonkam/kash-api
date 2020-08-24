from app import db
from models import mixins


class Banner(db.Model, mixins.BaseMixin):
    link = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False)
