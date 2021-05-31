# Generated by Django 3.1.1 on 2021-05-23 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kash', '0050_wallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='WalletFundingHistory',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('txn_ref', models.CharField(max_length=255, unique=True)),
                ('status', models.CharField(max_length=15)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kash.wallet')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]