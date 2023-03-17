# Generated by Django 4.1.7 on 2023-03-16 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agencies', '0002_alter_agency_lang_alter_agency_time_zone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monday', models.BooleanField()),
                ('tuesday', models.BooleanField()),
                ('wednesday', models.BooleanField()),
                ('thursday', models.BooleanField()),
                ('friday', models.BooleanField()),
                ('saturday', models.BooleanField()),
                ('sunday', models.BooleanField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agencies.agency')),
            ],
        ),
    ]
