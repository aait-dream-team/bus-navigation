# Generated by Django 4.1.7 on 2023-06-07 16:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('updater', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='alert_feed_id',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        )
    ]
