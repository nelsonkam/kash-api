from ariadne import QueryType
from sqlalchemy.orm import joinedload

from models import Shop, Product, Category, Banner

query = QueryType()


@query.field("shops")
def resolve_shops(obj, info, username=None, limit=None, offset=None):
    relations = ["owner", "products", "products.images", "products.category"]
    if username:
        return Shop.with_joined(*relations).filter_by(username=username).all()
    return Shop.with_joined(*relations).limit(limit).offset(offset).all()


@query.field("products")
def resolve_products(obj, info, id=None, limit=None, offset=None, order_by="-created_at"):
    print("obj", obj)
    relations = ["shop", "images", "category", "category.products"]
    if id:
        return Product.with_joined(*relations).filter_by(id=id).all()
    return Product.with_joined(*relations).order_by(*Product.order_expr(order_by)).limit(limit).offset(offset).all()


@query.field("categories")
def resolve_categories(obj, info, slug=None, limit=None, offset=None):
    relations = ["products", "products.images", "products.category"]
    if slug:
        return Category.with_joined(*relations).filter_by(slug=slug).all()
    return Category.with_joined(*relations).limit(limit).offset(offset).all()


@query.field("banners")
def resolve_banners(obj, info, id=None):
    if id:
        return Banner.where(id=id).all()
    return Banner.all()


@query.field("similar_products")
def resolve_similar_products(obj, info, product_id):
    product = Product.find_or_fail(product_id)
    return Product.query.join(Category).filter(Product.id!=product_id, Category.id==product.category_id).limit(4).all()


