# Generated by Django 3.1.1 on 2020-09-09 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200909_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='shipping_option',
            field=models.JSONField(blank=True, null=True),
        ),
    ]