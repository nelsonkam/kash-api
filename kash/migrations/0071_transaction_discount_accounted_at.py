# Generated by Django 3.1.1 on 2021-09-05 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kash', '0070_auto_20210905_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='discount_accounted_at',
            field=models.DateTimeField(null=True),
        ),
    ]