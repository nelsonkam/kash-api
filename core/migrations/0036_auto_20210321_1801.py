# Generated by Django 3.1.1 on 2021-03-21 18:01

from django.db import migrations
from djmoney.money import Money


def fill_prices_product(apps, schema_editor):
    Product = apps.get_model("core", "Product")
    for product in Product.objects.all():
        product.new_price = Money(product.price, product.shop.currency_iso)
        product.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20210321_1801'),
    ]

    operations = [
        migrations.RunPython(fill_prices_product)
    ]