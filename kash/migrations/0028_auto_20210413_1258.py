# Generated by Django 3.1.1 on 2021-04-13 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kash', '0027_fundinghistory_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='KashTransaction',
            new_name='SendKash',
        ),
    ]
