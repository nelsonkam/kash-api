# Generated by Django 3.1.1 on 2022-03-15 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kash_card", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="virtualcard",
            name="permablock_reason",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="virtualcard",
            name="is_permablocked",
            field=models.BooleanField(default=False),
        ),
    ]
