# Generated by Django 4.1.7 on 2023-06-15 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0007_admin_otp_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='user_type',
            field=models.CharField(choices=[('sys-admin', 'System Administrator'), ('admin', 'Administrator')], default='sys-admin', max_length=150),
        ),
    ]
