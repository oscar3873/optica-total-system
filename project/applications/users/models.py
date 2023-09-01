from django.db import models
#
from django.contrib.auth.models import AbstractUser
#
from .managers import UserManager
from applications.branches.models import Branch

class User(AbstractUser):
    ROLE = [
        ('ADMINISTRADOR', 'ADMINISTRADOR'),
        ('EMPLEADO', 'EMPLEADO')
    ]

    role = models.CharField(max_length=15, choices=ROLE, default='EMPLEADO', null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # Don't forget 'username' which is inherited from AbstractUser

    objects = UserManager()

    
    def __str__(self):
        return f"{self.get_full_name()} | {self.email or 'Sin email'}"
