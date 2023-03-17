# Generated by Django 4.1.7 on 2023-03-16 17:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stops', '0002_remove_stop_parent_station'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transfer_type', models.CharField(choices=[('dkn', "don't know"), ('now', 'dont')], max_length=100)),
                ('min_transfer_time', models.PositiveIntegerField()),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('from_stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_stop', to='stops.stop')),
                ('to_stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_stop', to='stops.stop')),
            ],
            options={
                'unique_together': {('from_stop', 'to_stop')},
            },
        ),
    ]
