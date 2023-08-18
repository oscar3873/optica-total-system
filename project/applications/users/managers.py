from django.db import models
#
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, role, username, email, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            role = role,
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, password, **extra_fields): # Para Empleados
        is_staff = False
        is_superuser = False
        role = 'EM'
        return self._create_user(role, username, email, password, is_staff, is_superuser, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields): # Para SuperAdmin (SALTACODE)
        is_staff = True
        is_superuser = True
        role = 'AD'
        return self._create_user(role, username, email, password, is_staff, is_superuser, **extra_fields)
    
    def create_admin(self, username, email, password, **extra_fields): # Para Admin (OPTICA-TOTAL)
        is_staff = True
        is_superuser = False
        role = 'AD'
        return self._create_user(role, username, email, password, is_staff, is_superuser, **extra_fields)
