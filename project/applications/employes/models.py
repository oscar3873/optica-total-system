from django.db import models

from applications.core.models import Person
from applications.branches.models import Branch

from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel



# Create your models here.
class Employee(SoftDeletionModel, TimestampsModel):
    """
    Clase de Empleados
        almacenamineto de datos de empleados con sus datos generales y a que surucrsal pertenece
    """
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    from_branch = models.ForeignKey(Branch, on_delete=models.PROTECT, null=True)
    address = models.CharField(max_length=120, blank=True, null=True)
