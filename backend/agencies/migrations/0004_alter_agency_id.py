# Generated by Django 4.1.7 on 2023-06-10 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agencies', '0003_alter_agency_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='id',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]