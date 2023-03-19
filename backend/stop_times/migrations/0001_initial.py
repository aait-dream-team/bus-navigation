# Generated by Django 4.1.7 on 2023-03-16 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agencies', '0003_alter_agency_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='StopTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_time', models.TimeField()),
                ('departure_time', models.TimeField()),
                ('stop_sequence', models.IntegerField()),
                ('stop_headsign', models.CharField(max_length=200)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agencies.agency')),
            ],
        ),
    ]