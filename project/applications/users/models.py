from django.db import models
#
from django.contrib.auth.models import AbstractUser
#
from .managers import *

class User(AbstractUser):
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, blank=True)
    lastname = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Don't forget 'username' which is inherited from AbstractUser

    objects = UserManager()
    
    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name + ' ' + self.lastname