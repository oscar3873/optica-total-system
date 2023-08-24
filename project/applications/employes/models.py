from django.db import models

from applications.core.models import Person
from applications.branches.models import Branch
from applications.users.models import User

from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel

# Create your models here.
class Employee(Person, SoftDeletionModel, TimestampsModel):
    """
    Clase de Empleados
        almacenamineto de datos de empleados con sus datos generales y a que surucrsal pertenece
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employee')
    user_made = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='from_employee')
    from_branch = models.ForeignKey(Branch, on_delete=models.PROTECT, null=True, related_name='employee')
    address = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self) -> str:
        return f'{self.get_full_name()}'