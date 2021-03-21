# Generated by Django 3.1.1 on 2021-03-21 18:10

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20210321_1807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='old_currency_iso',
        ),
        migrations.RemoveField(
            model_name='product',
            name='old_price',
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default_currency='XOF', max_digits=14),
        ),
    ]
