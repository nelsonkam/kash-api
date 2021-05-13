# Generated by Django 3.1.1 on 2021-05-10 20:11

from django.db import migrations


def create_wallets(apps, schema_editor):
    UserProfile = apps.get_model("kash", "UserProfile")
    Wallet = apps.get_model("kash", "Wallet")

    for profile in UserProfile.objects.all():
        wallet = Wallet(profile=profile)
        wallet.save()


class Migration(migrations.Migration):
    dependencies = [
        ('kash', '0050_wallet_wallettransaction'),
    ]

    operations = [
        migrations.RunPython(create_wallets)
    ]
