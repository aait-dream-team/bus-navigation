# Generated by Django 4.1.7 on 2023-03-26 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0001_initial'),
        ('stops', '0002_remove_stop_parent_station'),
        ('fares', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fare',
            name='end_stop',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='end_stops', to='stops.stop'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fare',
            name='route',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='routes.route'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fare',
            name='start_stop',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='start_stops', to='stops.stop'),
            preserve_default=False,
        ),
    ]