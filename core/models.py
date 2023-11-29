from django.db import models
from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from project.settings import DATE_NOW

# Create your models here.
class Person(SoftDeletionModel, TimestampsModel):
    """
    Clase para el almacenamiento de datos basicos de personas
    """
    first_name = models.CharField(max_length=50, verbose_name="Nombre")
    last_name = models.CharField(max_length=50, db_index=True, verbose_name="Apellido")
    phone_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="COD.Pais")
    phone_number = models.PositiveBigIntegerField(null=True, blank=True, verbose_name="Telefono")
    dni = models.CharField(max_length=20, db_index=True, null=True, blank=False, verbose_name="DNI")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Fecha")
    address = models.CharField(max_length=120, blank=True, null=True, verbose_name="Domicilio")
    email = models.EmailField(unique=False, null=True, blank=True, verbose_name="Correo")
    branch = models.ForeignKey('branches.Branch', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Sucursal")

    class Meta:
        abstract = True

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self) -> str:
        return f'{self.get_full_name()}\nDNI: {self.dni}'


class BaseAbstractWithUser(SoftDeletionModel, TimestampsModel):
    """
    Clase abstracta para todos los modelos
        Para registrar el usuario quien genero el objeto con fecha de creacion y edicion
    """
    user_made = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Por")

    class Meta:
        abstract = True
    
    def __str__(self) -> str:
        return f'Por: {self.user_made}'


class SaveGeneriModel(SoftDeletionModel, TimestampsModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
    

class Objetives(BaseAbstractWithUser):
    """
    Clase para los objetivos que tendran las Scursales y los empleados.
        title: Asunto del objetivo
        description: Detalles del objetivo a completar
        start_date/exp_date: Fecha de validez (desde el 1 al ultimo dia del mes)
        quantity: Objetivo al que se quiere llegar (cantidad de ventas o monetario)
    """
    PARA= [
        ('EMPLEADOS', 'EMPLEADOS'),
        ('SUCURSAL', 'SUCURSAL'),
    ]

    to = models.CharField(max_length=9, choices=PARA, default="EMPLEADOS", null=True, blank=True, verbose_name='Para')
    title = models.CharField(max_length=25, null=True, blank=True, verbose_name='Nombre')
    description = models.CharField(max_length=150, null=True, blank=True, verbose_name='Descripción')
    start_date = models.DateField(null=True, blank=True, verbose_name='Fecha de nicio')
    exp_date = models.DateField(null=True, blank=True, verbose_name='Fecha de finalizacion')
    quantity = models.PositiveIntegerField(null=True, blank=True, verbose_name='Objetivo')
    branch = models.ForeignKey('branches.Branch', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Sucursal")

    def __str__(self) ->str:
        return f'{self.title} - {self.start_date} a {self.exp_date} para {self.to}'
    
    def is_active(self) ->bool:
        return DATE_NOW.date() <= self.exp_date