from django.db import models

from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel

from applications.branches.managers import ObjectiveActiveBranchManager


# Create your models here.
class Branch(SoftDeletionModel, TimestampsModel):
    """
    Clase para Sucursales
        guarda datos generales de una sucursal
    """
    name = models.CharField(max_length=100, verbose_name='Nombre')
    address = models.CharField(max_length=100, verbose_name='Direccion')
    open_hs = models.TimeField(verbose_name='Horario de apertura')
    close_hs = models.TimeField(verbose_name='Horario de cierre')
    phone = models.CharField(max_length=20, verbose_name='Telefono', null=True, blank=True)

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"

    def __str__(self) -> str:
        return f'{self.name}\n- {self.address}\nHorarios: {self.open_hs} - {self.close_hs}'
    

class Branch_Objetives(SoftDeletionModel, TimestampsModel):
    """
    Clase intermedia para involuclar X cantidad de objetivos con una sucursal.
        is_completed: Indicador de Objetivo completado o no.
        employee: El objetivo es compleado por la sucursal
        objetive: Objetivo para la sucursal
        accumulated: Cantidad acumulada del objetivo
    """
    is_completed = models.BooleanField(default=False, blank=True, verbose_name='Completado')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Sucursal')
    objetive = models.ForeignKey('core.Objetives', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Objetivo')
    accumulated = models.PositiveIntegerField(default= 0, null=True, blank=True, verbose_name='Acumulado')

    active_objectives = ObjectiveActiveBranchManager()

    def ___str__(self) ->str:
        return f'{self.objetive} - {self.is_completed}'