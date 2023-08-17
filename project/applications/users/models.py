from django.db import models
#
from django.contrib.auth.models import AbstractUser
#
from .managers import UserManager

class User(AbstractUser):
    USER_ROLE = [
        ('AD','Administrador'),
        ('EM','Empleado')
    ]
    role = models.CharField(max_length=2, choices=USER_ROLE, default='EM')
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Don't forget 'username' which is inherited from AbstractUser

    objects = UserManager()
    
    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name + ' ' + self.lastname
    
    def __str__(self):
        return f"{self.username} | {self.email or 'Sin email'} | {self.name}"