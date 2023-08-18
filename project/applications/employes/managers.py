from django.db import models
from django.contrib.auth.models import BaseUserManager

class EmployeeManager(BaseUserManager, models.Manager):

    def create_user(self, user, **employee):
        """
        Crea y guarda un Empleado con el usuario y otros datos proporcionados.
        """
        employee = self.model(
            user= user,
            **employee
            )
        employee.save(using=self._db)
        return employee