from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

some_field = models.CharField(max_length=32, blank=True, null=True)
some_field.contribute_to_class(User, 'company')

location = models.CharField(max_length=32, blank=True, null=True)
location.contribute_to_class(User, 'location')

phone_number = models.IntegerField(blank=True, null=True)
phone_number.contribute_to_class(User, 'phone_number')
