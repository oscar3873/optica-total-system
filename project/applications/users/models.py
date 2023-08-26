from django.db import models
#
from django.contrib.auth.models import AbstractUser
#
from .managers import UserManager

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']  # Don't forget 'username' which is inherited from AbstractUser

    objects = UserManager()

    
    def __str__(self):
        return f"{self.get_full_name()} | {self.email or 'Sin email'}"