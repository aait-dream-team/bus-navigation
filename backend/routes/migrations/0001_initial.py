# Generated by Django 4.1.7 on 2023-03-16 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agencies', '0002_alter_agency_lang_alter_agency_time_zone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_short_name', models.CharField(max_length=200)),
                ('route_long_name', models.CharField(max_length=300)),
                ('route_desc', models.CharField(max_length=500)),
                ('route_type', models.CharField(choices=[('car', 'Roads'), ('air', 'AirPlanes')], max_length=200)),
                ('route_url', models.URLField()),
                ('route_color', models.CharField(max_length=20)),
                ('route_text_color', models.CharField(max_length=20)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agencies.agency')),
            ],
        ),
    ]
