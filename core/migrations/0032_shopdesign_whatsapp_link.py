# Generated by Django 3.1.1 on 2021-03-18 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20210311_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopdesign',
            name='whatsapp_link',
            field=models.URLField(blank=True),
        ),
    ]
