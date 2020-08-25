from app import db
from models import mixins


class ProductImage(mixins.BaseModel):
    url = db.Column(db.Text, nullable=False)
    product_id = mixins.foreign_key("product")
