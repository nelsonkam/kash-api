import re

from app import create_app, db
from models import Product

app = create_app()

def fix_db():
    with app.app_context():
        for product in Product.all():
            Product.set_session(db.session)
            product.price = re.sub('[^0-9]','', product.price)
            print(product.price)
            product.save()
