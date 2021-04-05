# Generated by Django 3.1.1 on 2021-04-04 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('kash', '0012_payoutmethod'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('object_id', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('sent_at', models.DateTimeField(null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='kash.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]