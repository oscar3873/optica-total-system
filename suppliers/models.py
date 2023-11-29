from django.db import models

from core.models import BaseAbstractWithUser
from products.models import Brand
from .managers import SupplierManager

""" 
# Para validar un número de telefono
from django.core.validators import RegexValidator
"""


# Create your models here.
class Supplier(BaseAbstractWithUser):
    """ # Para validar un número de telefono
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$") """
    name = models.CharField(max_length=50, verbose_name='Razón Social', null=True, blank=True)
    phone_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="COD.Pais")
    phone_number = models.BigIntegerField(verbose_name='Telefono de contacto', null=True, blank=True)
    email = models.EmailField(verbose_name='Correo electronico', null=True, blank=True)
    address = models.CharField(max_length=50, verbose_name='Dirección', null=True, blank=True)
    
    objects = SupplierManager()

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self) -> str:
        return f'{self.name} | {self.phone_number} | {self.email}'
    


class Brand_Supplier(BaseAbstractWithUser):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='brand_suppliers', null=True, verbose_name='Proveedor')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_suppliers', null=True, verbose_name='Marca')

    class Meta:
        verbose_name = "Marca por Proveedor"

    def __str__(self):
        return f'{self.supplier.name} | {self.brand.name}'


class Bank(BaseAbstractWithUser):
    bank_name = models.CharField(unique=True, max_length=50, verbose_name='Nombre del Banco')

    class Meta:
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"

    def __str__(self) -> str:
        return f'{self.bank_name}'
    
    
class Cbu(models.Model):
    cbu = models.CharField(unique=True, max_length=20, verbose_name='ALIAS/CBU/CVU')
    cuit = models.CharField(max_length=20, blank=True, null=True, verbose_name='CUIT Proveedor')
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='cbu', blank=True, null=True, verbose_name='Banco')
    
    class Meta:
        verbose_name = "ALIAS / CBU / CVU"

    def __str__(self) -> str:
        return f'{self.bank.__str__()} | {self.cbu}'


class Supplier_Bank(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='banks', null=True, verbose_name='Proveedor')
    bank = models.OneToOneField(Cbu, on_delete=models.CASCADE, related_name='suppliers', null=True, verbose_name='Banco asociado')

    def __str__(self) -> str:
        return f'{self.supplier.name} | {self.bank.__str__()}'