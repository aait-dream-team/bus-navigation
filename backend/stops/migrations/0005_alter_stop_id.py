# Generated by Django 4.1.7 on 2023-06-13 19:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0004_remove_stop_location_type_alter_stop_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stop',
            name='id',
            field=models.CharField(default=uuid.uuid4, max_length=200, primary_key=True, serialize=False),
        ),
    ]