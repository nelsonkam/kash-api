# Generated by Django 3.1.1 on 2020-09-16 12:54

import core.models.base
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_shop_cover_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='avatar_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='cover_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='AffiliateAgent',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(default=core.models.base.generate_affiliate_code, max_length=10)),
                ('momo_number', models.CharField(max_length=255, null=True)),
                ('avatar_url', models.URLField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='affiliate', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'affiliate_agents',
            },
        ),
        migrations.AddField(
            model_name='shop',
            name='affiliate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shops', to='core.affiliateagent'),
        ),
    ]
