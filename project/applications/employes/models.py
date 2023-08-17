from django.db import models

from applications.core.models import Person
from applications.branches.models import Branch
from applications.users.models import User

from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel

from .managers import EmployeeManager

# Create your models here.
class Employee(Person, SoftDeletionModel, TimestampsModel):
    """
    Clase de Empleados
        almacenamineto de datos de empleados con sus datos generales y a que surucrsal pertenece
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    from_branch = models.ForeignKey(Branch, on_delete=models.PROTECT, null=True)
    address = models.CharField(max_length=120, blank=True, null=True)

    objects = EmployeeManager()

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self) -> str:
        return f'{self.get_full_name()}'