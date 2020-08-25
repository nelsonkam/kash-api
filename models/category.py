from app import db
from models import mixins


class Category(mixins.BaseModel):
    name = db.Column(db.Text, nullable=False, unique=True)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    products = db.relationship("Product", backref='category')

