# Generated by Django 3.1.1 on 2021-03-21 19:50

from django.db import migrations
from djmoney.money import Money


def fill_prices_order_items(apps, schema_editor):
    OrderItem = apps.get_model("core", "OrderItem")
    for item in OrderItem.objects.all():
        item.price = item.product.price
        item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20210321_1949'),
    ]

    operations = [
        migrations.RunPython(fill_prices_order_items)
    ]