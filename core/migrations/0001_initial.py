# Generated by Django 3.1.1 on 2020-09-09 00:07

import core.models.base
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('link', models.TextField()),
                ('image_url', models.TextField()),
            ],
            options={
                'db_table': 'banners',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uid', models.CharField(default=core.models.base.generate_uid, max_length=40, unique=True)),
            ],
            options={
                'db_table': 'carts',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.TextField(unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'db_table': 'categories',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=255, null=True, unique=True)),
            ],
            options={
                'db_table': 'customers',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('price', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('currency_iso', models.CharField(max_length=10)),
                ('slug', models.CharField(max_length=255, unique=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.category')),
            ],
            options={
                'db_table': 'products',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(max_length=255)),
                ('avatar_url', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'users',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('avatar_url', models.TextField(blank=True, null=True)),
                ('whatsapp_number', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('phone_number', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
            options={
                'db_table': 'shops',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('url', models.URLField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
            options={
                'db_table': 'product_images',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.shop'),
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('uid', models.CharField(max_length=40, unique=True)),
                ('shipping_option', models.TextField(blank=True, null=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cart')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.customer')),
            ],
            options={
                'db_table': 'checkouts',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
            options={
                'db_table': 'cart_items',
                'managed': True,
            },
        ),
    ]