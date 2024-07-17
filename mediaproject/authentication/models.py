from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group

from django.db import models
from django.utils import timezone

class User(AbstractUser):
    username = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    profile_img = models.ImageField(upload_to='profile', blank=True, null=True)
    sub_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True,)
    roles = models.CharField(max_length=15, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    groups = models.ManyToManyField(Group, related_name='custom_user')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')