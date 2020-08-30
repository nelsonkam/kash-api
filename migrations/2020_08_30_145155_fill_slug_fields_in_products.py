import secrets

from orator.migrations import Migration
from slugify import slugify


class FillSlugFieldsInProducts(Migration):

    def up(self):
        """
        Run the migrations.
        """
        from models import Product
        for product in Product.all():
            product.slug = slugify(product.name) + '-' + secrets.token_hex(2)
            product.save()


    def down(self):
        """
        Revert the migrations.
        """
        pass
