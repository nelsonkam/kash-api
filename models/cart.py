from app import db


# class Cart(db.Model):
#     pass
#
#
# class Item(db.Model):
#     cart_id = mixins.foreign_key("cart")
#     quantity = db.Column(db.Integer)
#     total = db.Column(db.Integer)
#     product_id = mixins.foreign_key("product")
#
#
#     def compute_total(self):
#         from models import Product
#         product = Product.find_or_fail(self.product_id)
#         return product.price * self.quantity
