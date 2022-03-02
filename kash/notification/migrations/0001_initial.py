# Generated by Django 3.1.1 on 2022-02-28 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('kash_user', '0001_initial'),
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
                ('content_type',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('profile',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications',
                                   to='kash_user.userprofile')),
            ],
            options={
                'abstract': False,
                'db_table': 'kash_notification'
            },
        ),
    ]
