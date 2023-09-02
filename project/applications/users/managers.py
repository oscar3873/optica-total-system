from django.db import models
#
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def all(self):
        users_active = self.model.filter(is_active=True)
        return users_active

    def _create_user(self, first_name, last_name, username, email, password, is_staff, is_superuser, role, branch=None, **extra_fields):
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            role= role,
            branch = branch,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, first_name, last_name, username, email, password, branch, **extra_fields): # Para Empleados
        is_staff = False
        is_superuser = False
        role = 'EMPLEADO'
        return self._create_user(first_name, last_name, username, email, password, is_staff, is_superuser, role, branch, **extra_fields)

    def create_superuser(self, first_name, last_name, username, email, password, branch=None, **extra_fields): # Para SuperAdmin (SALTACODE)
        is_staff = True
        is_superuser = True
        role = 'ADMINISTRADOR'
        return self._create_user(first_name, last_name, username, email, password, is_staff, is_superuser, role, branch, **extra_fields)
    
    def create_admin(self, first_name, last_name, username, email, password, branch=None, **extra_fields): # Para Admin (OPTICA-TOTAL)
        is_staff = True
        is_superuser = False
        role = 'ADMINISTRADOR'
        return self._create_user(first_name, last_name, username, email, password, is_staff, is_superuser, role, branch, **extra_fields)
