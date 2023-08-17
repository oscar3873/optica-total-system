from django.db import models
from applications.core.models import Person
from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel

from .managers import CustomerManager

# Create your models here.
class HealthInsurance(SoftDeletionModel, TimestampsModel):
    """
    Clase para Obras Sociales
        se guardan datos basicos del cada obra social
    """
    name = models.CharField(max_length=50, db_index=True)
    cuit = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f'Obra Social: {self.name} - CUIT: {self.cuit}'


class Customer(SoftDeletionModel, TimestampsModel):
    """
    Clase para Clientes
        se guardan datos para almacenar clientes:
            -person: clave foranea de la Clase generica de Personas (datos generales)
            -address: direccion del cliente
    """
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    address = models.CharField(max_length=200)

    objects = CustomerManager()

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self) -> str:
        return f'{self.person.last_name}, {self.person.name} - Email: {self.address}'
    

class Customer_HealthInsurance(SoftDeletionModel, TimestampsModel):
    """
    Clase intermedia para Clientes y sus Obras sociales
    """
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='customer_insurance')
    h_insurance = models.ForeignKey(HealthInsurance, on_delete=models.PROTECT, related_name='customer_insurance')

    def __str__(self) -> str:
        return f'Cliente: {self.customer}\nObra Social: {self.h_insurance}'


class MedicalHistory(SoftDeletionModel, TimestampsModel):
    """
    Clase de Historial Medico
        se almacenan los datos de la historia clinica de los clientes para brindarles
        los productos acorde a sus necesidades
            -customer: cliente asociado
            -diagnostic: diagnostico del cliente
    """
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='medical_history')
    diagnostic = models.CharField(max_length=250)

    def __str__(self) -> str:
        return (f'Cliente: {self.customer}\n' +
                f'Diagnostico: {self.diagnostic}')
