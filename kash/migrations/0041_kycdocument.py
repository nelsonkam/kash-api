# Generated by Django 3.1.1 on 2021-04-20 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kash', '0040_auto_20210419_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='KYCDocument',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id_doc_url', models.URLField(null=True)),
                ('id_document_type', models.CharField(max_length=25)),
                ('selfie_url', models.URLField(null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=30)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kash.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]