# Generated by Django 3.1.1 on 2021-08-06 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kash', '0061_auto_20210806_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundinghistory',
            name='retries',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
