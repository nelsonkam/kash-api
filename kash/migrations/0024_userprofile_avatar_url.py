# Generated by Django 3.1.1 on 2021-04-07 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kash', '0023_auto_20210406_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar_url',
            field=models.URLField(blank=True),
        ),
    ]
