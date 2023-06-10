from datetime import datetime
import pytz
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from random import choice

USER_TYPES = [("sys-admin", "System Administrator"), ("admin", "Administrator")]


class Admin(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(choices=USER_TYPES, max_length=150, default=USER_TYPES[0])
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'
    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items_for_otp = []
        for i in range(6):
            num = choice(number_list)
            code_items_for_otp.append(num)

        code_string = "".join(str(item) for item in code_items_for_otp)
        
        self.email = self.username
        self.otp = code_string
        self.otp_created_at = datetime.now(pytz.timezone('America/New_York'))
        return super().save(*args, **kwargs)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)