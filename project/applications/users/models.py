from django.db import models
#
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
#
from .managers import UserManager
from applications.branches.models import Branch

from applications.core.models import Person

class User(Person, AbstractUser):
    ROLE = [
        ('ADMINISTRADOR', 'ADMINISTRADOR'),
        ('EMPLEADO', 'EMPLEADO')
    ]

    role = models.CharField(max_length=15, choices=ROLE, default='EMPLEADO', null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = UserManager()

    
    def __str__(self):
        return f"{self.get_full_name()} | {self.email or 'Sin email'}"
