from app import db
from models import mixins


class Cart(mixins.BaseModel):
    items = db.relationship("Item", backref="cart")
    # ordered = db.Column(db.Boolean, nullable=False, default=False)


class Item(mixins.BaseModel):
    cart_id = mixins.foreign_key("cart")
    quantity = db.Column(db.Integer)
    total = db.Column(db.Integer)
    product_id = mixins.foreign_key("product")


    def compute_total(self):
        from models import Product
        product = Product.find_or_fail(self.product_id)
        return product.price * self.quantity
