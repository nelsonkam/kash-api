# Generated by Django 3.1.1 on 2021-08-07 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kash', '0063_auto_20210806_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualcard',
            name='provider_name',
            field=models.CharField(choices=[('rave', 'Rave'), ('dummy', 'Dummy')], default='rave', max_length=20),
        ),
    ]