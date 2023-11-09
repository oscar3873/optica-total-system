from django.db import models

from applications.core.models import BaseAbstractWithUser
from applications.products.models import Brand
from .managers import SupplierManager

""" 
# Para validar un número de telefono
from django.core.validators import RegexValidator
"""


# Create your models here.
class Supplier(BaseAbstractWithUser):
    """ # Para validar un número de telefono
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$") """
    phone_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="COD.Pais")
    phone_number = models.BigIntegerField(unique=True ,verbose_name='Telefono de contacto', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='Razón Social', null=True, blank=True)
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
    cbu = models.CharField(max_length=20, verbose_name='CBU')
    bank_name = models.CharField(max_length=50, verbose_name='Nombre del Banco')
    cuit = models.CharField(max_length=20, verbose_name='CUIT', blank=True, null=True)

    class Meta:
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"

    def __str__(self) -> str:
        return f'{self.bank_name} | {self.cbu}'
    

class Supplier_Bank(BaseAbstractWithUser):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='banks', null=True, verbose_name='Proveedor')
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='supplier', null=True, verbose_name='Banco')

    def __str__(self) -> str:
        return f'{self.supplier.name} | {self.bank.bank_name} - ALIAS/CBU: {self.bank.cbu}'