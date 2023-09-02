from django.db import models

# Create your models here.
class Branch(models.Model):
    """
    Clase para Sucursales
        guarda datos generales de una sucursal
    """
    name = models.CharField(max_length=100, verbose_name='Nombre')
    address = models.CharField(max_length=100, verbose_name='Direccion')
    open_hs = models.TimeField(verbose_name='Horario de apertura')
    close_hs = models.TimeField(verbose_name='Horario de cierre')

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"

    def __str__(self) -> str:
        return f'{self.name}\n- {self.address}\nHorarios: {self.open_hs} - {self.close_hs}'
    