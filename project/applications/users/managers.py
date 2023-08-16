from django.db import models
#
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, password=None, **extra_fields): # Para Empleados
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields): # Para SuperAdmin (SALTACODE)
        return self._create_user(username, email, password, True, True, **extra_fields)
    
    def create_admin(self, username, email, password=None, **extra_fields): # Para Admin (OPTICA-TOTAL)
        return self._create_user(username, email, password, True, False, **extra_fields)