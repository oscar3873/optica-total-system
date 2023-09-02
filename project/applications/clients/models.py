from django.db import models
from django.urls import reverse
from applications.core.models import Person
from applications.core.models import BaseAbstractWithUser

from applications.users.models import User
from .managers import CustomerManager, LabManager


# Create your models here.
class HealthInsurance(BaseAbstractWithUser):
    """
    Clase para Obras Sociales
        se guardan datos basicos del cada obra social
    """
    name = models.CharField(max_length=50, db_index=True)
    phone_number = models.PositiveBigIntegerField(null=True, blank=True)
    cuit = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Obra Socail"
        verbose_name_plural = "Obras Socailes"

    def __str__(self) -> str:
        return f'Obra Social: {self.name} - CUIT: {self.cuit}'


class Customer(Person, BaseAbstractWithUser):
    """
    Clase para Clientes
        se guardan datos para almacenar clientes
    """
    objects = CustomerManager()

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self) -> str:
        return f'{self.last_name}, {self.first_name}'
    
    def get_absolute_url(self):
        return reverse('clients_app:detail', kwargs={'pk': self.pk})
    

class Customer_HealthInsurance(BaseAbstractWithUser):
    """
    Clase intermedia para Clientes y sus Obras sociales
    """
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='customer_insurance')
    h_insurance = models.ForeignKey(HealthInsurance, on_delete=models.PROTECT, related_name='customer_insurance')

    def __str__(self) -> str:
        return f'Cliente: {self.customer}\nObra Social: {self.h_insurance}'


class Correction(BaseAbstractWithUser):
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

class Material(BaseAbstractWithUser):
    policarbonato = models.BooleanField(null=True, blank=True)
    organic = models.BooleanField(null=True, blank=True)
    mineral = models.BooleanField(null=True, blank=True)
    m_r8 = models.BooleanField(null=True, blank=True)


class Color(BaseAbstractWithUser):
    white = models.BooleanField(null=True, blank=True)
    full_gray = models.BooleanField(null=True, blank=True)
    gray_gradient = models.BooleanField(null=True, blank=True)
    flat_sepia = models.BooleanField(null=True, blank=True)

class Cristal(BaseAbstractWithUser):
    monofocal = models.BooleanField(null=True, blank=True)
    bifocal_fv = models.BooleanField(null=True, blank=True)
    bifocal_k = models.BooleanField(null=True, blank=True)
    bifocal_pi = models.BooleanField(null=True, blank=True)
    progressive = models.BooleanField(null=True, blank=True)

class Tratamient(BaseAbstractWithUser):
    antireflex = models.BooleanField(null=True, blank=True)
    filtro_azul = models.BooleanField(null=True, blank=True)
    fotocromatico = models.BooleanField(null=True, blank=True)
    ultravex = models.BooleanField(null=True, blank=True)
    polarizado = models.BooleanField(null=True, blank=True)
    neutrosolar = models.BooleanField(null=True, blank=True)
    
###############################################################

class Interpupillary(BaseAbstractWithUser):
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

class Calibration_Order(BaseAbstractWithUser):
    is_done = models.BooleanField(default=False, null=True, blank=True)
    correction = models.ForeignKey(Correction, on_delete=models.PROTECT, related_name='laboratory', null=True, blank=True)
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='laboratory', null=True, blank=True)
    type_cristal = models.ForeignKey(Cristal, on_delete=models.PROTECT, related_name='laboratory', null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.PROTECT, related_name='laboratory', null=True, blank=True)
    tratamient = models.ForeignKey(Tratamient, on_delete=models.PROTECT, related_name='laboratory', null=True, blank=True)
    interpupillary = models.ForeignKey(Interpupillary, on_delete=models.PROTECT, related_name='laboratory', null = True, blank=True)
    diagnostic = models.CharField(max_length=200, null=True, blank=True)
    armazon = models.CharField(max_length=100, null=True, blank=True)
    observations = models.CharField(max_length=200, null=True, blank=True)

    objects = LabManager()
