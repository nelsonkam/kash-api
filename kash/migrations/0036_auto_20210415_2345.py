# Generated by Django 3.1.1 on 2021-04-15 23:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kash', '0035_auto_20210415_2335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kashrequest',
            name='recipients',
        ),
        migrations.AlterField(
            model_name='kashrequest',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kash_requests', to='kash.userprofile'),
        ),
    ]