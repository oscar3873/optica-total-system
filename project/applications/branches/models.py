from django.db import models
from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel

# Create your models here.
class Branch(SoftDeletionModel, TimestampsModel):
    """
    Clase para Sucursales
        guarda datos generales de una sucursal
    """
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    open_hs = models.TimeField(verbose_name='Horario de apertura')
    close_hs = models.TimeField(verbose_name='Horario de cierre')

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"

    def __str__(self) -> str:
        return f'{self.name}\n- {self.address}\nHorarios: {self.open_hs} - {self.close_hs}'
    