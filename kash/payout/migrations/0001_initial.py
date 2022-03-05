# Generated by Django 3.1.1 on 2022-02-28 16:46

from django.db import migrations, models
import django.db.models.deletion
import kash.abstract.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("kash_user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AdminPayoutRequest",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "code",
                    models.CharField(
                        default=kash.abstract.models.generate_ref_id,
                        max_length=12,
                        unique=True,
                    ),
                ),
                ("phone", models.CharField(max_length=255)),
                ("gateway", models.CharField(max_length=255)),
                ("amount", models.IntegerField()),
            ],
            options={"abstract": False, "db_table": "kash_adminpayoutrequest"},
        ),
        migrations.CreateModel(
            name="Rate",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("code", models.CharField(max_length=100)),
                ("value", models.DecimalField(decimal_places=4, max_digits=17)),
            ],
            options={"abstract": False, "db_table": "kash_rate"},
        ),
    ]
