# Generated by Django 3.1.1 on 2021-04-06 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kash', '0016_kashtransaction_paid_recipients'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundingHistory',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('txn_ref', models.CharField(max_length=255)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kash.virtualcard')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]