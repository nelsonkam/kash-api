# Generated by Django 3.1.1 on 2021-04-07 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kash', '0024_userprofile_avatar_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundinghistory',
            name='txn_ref',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
