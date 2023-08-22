from django.db import models
from applications.core.models import Person
from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel
from applications.employes.models import Employee

from .managers import CustomerManager

# Create your models here.
class HealthInsurance(SoftDeletionModel, TimestampsModel):
    """
    Clase para Obras Sociales
        se guardan datos basicos del cada obra social
    """
    name = models.CharField(max_length=50, db_index=True)
    cuit = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Obra Socail"
        verbose_name_plural = "Obras Socailes"

    def __str__(self) -> str:
        return f'Obra Social: {self.name} - CUIT: {self.cuit}'


class Customer(Person, SoftDeletionModel, TimestampsModel):
    """
    Clase para Clientes
        se guardan datos para almacenar clientes:
            -address: direccion del cliente
    """
    address = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    objects = CustomerManager()

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self) -> str:
        return f'{self.last_name}, {self.name}'
    

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

    class Meta:
        verbose_name = "Historia medico"
        verbose_name_plural = "Historiales Medico"

    def __str__(self) -> str:
        return (f'Cliente: {self.customer}\n' +
                f'Diagnostico: {self.diagnostic}')


class Correction(SoftDeletionModel, TimestampsModel):
    lej_od_esferico = models.CharField(max_length=10, null=True, blank=True)
    lej_od_cilindrico = models.CharField(max_length=10, null=True, blank=True)
    lej_od_eje = models.CharField(max_length=10, null=True, blank=True)
    lej_oi_esferico = models.CharField(max_length=10, null=True, blank=True)
    lej_oi_cilindrico = models.CharField(max_length=10, null=True, blank=True)
    lej_oi_eje = models.CharField(max_length=10, null=True, blank=True)
    cer_od_esferico = models.CharField(max_length=10, null=True, blank=True)
    cer_od_cilindrico = models.CharField(max_length=10, null=True, blank=True)
    cer_od_eje = models.CharField(max_length=10, null=True, blank=True)
    cer_oi_esferico = models.CharField(max_length=10, null=True, blank=True)
    cer_oi_cilindrico = models.CharField(max_length=10, null=True, blank=True)
    cer_oi_eje = models.CharField(max_length=10, null=True, blank=True)
    
###############################################################

class Material(SoftDeletionModel, TimestampsModel):
    policarbonato = models.BooleanField()
    organic = models.BooleanField()
    mineral = models.BooleanField()
    m_r8 = models.BooleanField()

class Color(SoftDeletionModel, TimestampsModel):
    white = models.BooleanField()
    full_gray = models.BooleanField()
    gray_gradient = models.BooleanField()
    flat_sepia = models.BooleanField()

class Cristal(SoftDeletionModel, TimestampsModel):
    monofocal = models.BooleanField()
    bifocal_fv = models.BooleanField()
    bifocal_k = models.BooleanField()
    bifocal_pi = models.BooleanField()
    progressive = models.BooleanField()

class Tratamient(SoftDeletionModel, TimestampsModel):
    antireflex = models.BooleanField()
    filtro_azul = models.BooleanField()
    fotocromatico = models.BooleanField()
    ultravex = models.BooleanField()
    polarizado = models.BooleanField()
    neutrosolar = models.BooleanField()
    
###############################################################

class Interpupillary(SoftDeletionModel, TimestampsModel):
    lej_od_nanopupilar = models.CharField(max_length=10, null=True, blank=True)
    lej_od_pelicula = models.CharField(max_length=10, null=True, blank=True)
    lej_oi_nanopupilar = models.CharField(max_length=10, null=True, blank=True)
    lej_oi_pelicula = models.CharField(max_length=10, null=True, blank=True)
    lej_total = models.CharField(max_length=10, null=True, blank=True)
    cer_od_nanopupilar = models.CharField(max_length=10, null=True, blank=True)
    cer_od_pelicula = models.CharField(max_length=10, null=True, blank=True)
    cer_oi_nanopupilar = models.CharField(max_length=10, null=True, blank=True)
    cer_oi_pelicula = models.CharField(max_length=10, null=True, blank=True)
    cer_total = models.CharField(max_length=10, null=True, blank=True)
    
###############################################################

class Calibration_Order(SoftDeletionModel, TimestampsModel):
    is_done = models.BooleanField(default=False)
    correction = models.ForeignKey(Correction, on_delete=models.PROTECT, related_name='laboratory', null=True)
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='laboratory')
    type_cristal = models.ForeignKey(Cristal, on_delete=models.PROTECT, related_name='laboratory')
    color = models.ForeignKey(Color, on_delete=models.PROTECT, related_name='laboratory')
    tratamient = models.ForeignKey(Tratamient, on_delete=models.PROTECT, related_name='laboratory')
    interpupillary = models.ForeignKey(Interpupillary, on_delete=models.PROTECT, related_name='laboratory', null = True)
    medical_details = models.ForeignKey(MedicalHistory, on_delete=models.PROTECT, related_name='laboratory')
    employees = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='laboratory')
    armazon = models.CharField(max_length=100)
    observations = models.CharField(max_length=200)
