# Generated by Django 4.1.7 on 2023-04-01 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0002_remove_stop_parent_station'),
    ]

    operations = [
        migrations.AddField(
            model_name='stop',
            name='parent_station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stops.stop'),
        ),
    ]
