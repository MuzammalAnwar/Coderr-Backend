from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    class Usertype(models.TextChoices):
        CUSTOMER = 'customer'
        BUSINESS = 'business'

    type = models.CharField(
        choices=Usertype.choices,
        max_length=20
    )

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    tel = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.CharField(max_length=255, blank=True, default='')
    uploaded_at = models.DateTimeField(default=timezone.now, editable=False)
