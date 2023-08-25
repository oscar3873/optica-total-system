from django.db import models
#
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, name, last_name, username, email, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            first_name = name,
            last_name = last_name,
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, name, last_name, username, email, password, **extra_fields): # Para Empleados
        is_staff = False
        is_superuser = False
        return self._create_user(name, last_name, username, email, password, is_staff, is_superuser, **extra_fields)

    def create_superuser(self, name, last_name, username, email, password, **extra_fields): # Para SuperAdmin (SALTACODE)
        is_staff = True
        is_superuser = True
        return self._create_user(name, last_name, username, email, password, is_staff, is_superuser, **extra_fields)
    
    def create_admin(self, name, last_name, username, email, password, **extra_fields): # Para Admin (OPTICA-TOTAL)
        is_staff = True
        is_superuser = False
        return self._create_user(name, last_name, username, email, password, is_staff, is_superuser, **extra_fields)
