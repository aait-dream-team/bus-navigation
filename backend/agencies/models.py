import uuid
from django.db import models
from admins.models import Admin 
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


LANG = (("en", "English"), ("amh", "Amharic"))
TIME_ZONE = (("+3", "UTC+3"),)

class Agency(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    time_zone = models.CharField(choices=TIME_ZONE, max_length=200)
    lang = models.CharField(choices=LANG, max_length=200)
    phone = models.CharField(max_length=20)
    admin = models.ForeignKey(to = Admin, on_delete=models.CASCADE, unique=True)
    
    def __str__(self):
        return f'{self.name} ID: {self.id} Admin: {self.admin}'
