# Generated by Django 4.1.7 on 2023-06-10 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0003_stop_parent_station'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stop',
            name='location_type',
        ),
        migrations.AlterField(
            model_name='stop',
            name='id',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
