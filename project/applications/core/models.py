from django.db import models
from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel
from .managers import PersonManager

# Create your models here.
class Person(SoftDeletionModel, TimestampsModel):
    """
    Clase para el almacenamiento de datos basicos de personas
    """
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, db_index=True)
    phone_number = models.PositiveBigIntegerField(null=True, blank=True)
    dni = models.CharField(max_length=20, db_index=True)
    email = models.EmailField(max_length=55, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=120, blank=True, null=True)

    objects = PersonManager()

    def get_full_name(self):
        return f'{self.last_name}, {self.name}'

    def __str__(self) -> str:
        return f'{self.get_full_name()}\nDNI: {self.dni}'

    
