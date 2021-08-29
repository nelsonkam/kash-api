# Generated by Django 3.1.1 on 2021-08-26 08:11

from kash.models.user_profile import generate_code
from django.db import migrations


def fill_referral_code(apps, schema_editor):
    UserProfile = apps.get_model("kash", "UserProfile")

    for profile in UserProfile.objects.all():
        profile.referral_code = generate_code()
        profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('kash', '0066_auto_20210826_0809'),
    ]

    operations = [
        migrations.RunPython(fill_referral_code)
    ]
