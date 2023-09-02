from django.db import models
from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel

# Create your models here.
class Person(SoftDeletionModel, TimestampsModel):
    """
    Clase para el almacenamiento de datos basicos de personas
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, db_index=True)
    phone_number = models.PositiveBigIntegerField(null=True, blank=True)
    dni = models.CharField(max_length=20, db_index=True, null=True, blank=False)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    class Meta:
        abstract = True

    def get_full_name(self):
        return f'{self.last_name}, {self.first_name}'

    def __str__(self) -> str:
        return f'{self.get_full_name()}\nDNI: {self.dni}'
 

class BaseAbstractWithUser(SoftDeletionModel, TimestampsModel):
    """
    Clase abstracta para todos los modelos
        Para registrar el usuario quien genero el objeto con fecha de creacion y edicion
    """
    user_made = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        abstract = True
    
    def __str__(self) -> str:
        return f'Por: {self.user_made}'
