# Generated by Django 3.1.1 on 2021-04-19 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kash', '0037_auto_20210417_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='kashtransaction',
            name='txn',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='kash.transaction'),
        ),
    ]
