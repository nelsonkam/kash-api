# Generated by Django 3.1.1 on 2021-04-09 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kash', '0026_withdrawalhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundinghistory',
            name='status',
            field=models.CharField(default='success', max_length=15),
            preserve_default=False,
        ),
    ]