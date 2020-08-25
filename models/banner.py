from app import db
from models import mixins


class Banner(mixins.BaseModel):
    link = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False)
