from ariadne import QueryType

from models import Shop, Product, Category, Banner

query = QueryType()


@query.field("shops")
def resolve_shops(obj, info, username=None, limit=None, offset=0):
    relations = ["owner", "products", "products.images", "products.category"]
    if username:
        return Shop.with_(*relations).where('username', username).get().serialize()
    return Shop.with_(*relations).limit(limit).offset(offset).get().serialize()


@query.field("products")
def resolve_products(obj, info, slug=None, limit=None, offset=0, order_by="-created_at"):
    print("obj", obj)
    relations = ["shop", "images", "category", "category.products"]
    if id:
        return Product.with_(*relations).where('slug', slug).get().serialize()
    return Product.with_(*relations).order_by('created_at', 'desc').limit(limit).offset(offset).get().serialize()


@query.field("categories")
def resolve_categories(obj, info, slug=None, limit=None, offset=0):
    relations = ["products", "products.images", "products.category"]
    if slug:
        return Category.with_(*relations).where('slug', slug).get().serialize()
    return Category.with_(*relations).limit(limit).offset(offset).get().serialize()


@query.field("banners")
def resolve_banners(obj, info, id=None):
    if id:
        return Banner.where('id', id).all()
    return Banner.all()


@query.field("similar_products")
def resolve_similar_products(obj, info, product_id):
    product = Product.find(product_id)
    return Product.where("id", "!=", product_id).where_has('category', lambda q: q.where('id', product.category_id)).limit(4).get().serialize()




