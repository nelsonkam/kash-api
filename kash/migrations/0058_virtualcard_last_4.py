# Generated by Django 3.1.1 on 2021-07-21 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kash', '0057_auto_20210708_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualcard',
            name='last_4',
            field=models.CharField(blank=True, max_length=4),
        ),
    ]
