# Generated by Django 4.1.7 on 2023-06-07 16:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updater', '0005_remove_alert_start_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='start_timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
