# Generated by Django 3.1.1 on 2021-04-15 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kash', '0031_auto_20210415_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='momoaccount',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='momo_accounts', to='kash.userprofile'),
        ),
    ]