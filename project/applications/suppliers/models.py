from django.db import models

from applications.core.models import BaseAbstractWithUser
from applications.products.models import Product
from .managers import SupplierManager

""" 
# Para validar un número de telefono
from django.core.validators import RegexValidator
"""


# Create your models here.
class Supplier(BaseAbstractWithUser):
    """ # Para validar un número de telefono
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$") """
    phone_number = models.BigIntegerField(unique=True ,verbose_name='Telefono de contacto')
    name = models.CharField(max_length=50, verbose_name='Nombre')
    email = models.EmailField(verbose_name='Correo electronico', null=True, blank=True)

    objects = SupplierManager()

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self) -> str:
        return f'{self.name} | {self.phone_number} | {self.email}'
    

class Product_Supplier(BaseAbstractWithUser):
    """
    Clase intermedia de Producto y Proveedor almacenando sus PK para sus posteriores analisis
    """
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_suppliers', null=True, verbose_name='Producto')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='product_suppliers', null=True, verbose_name='Proveedor')

    def __str__(self) -> str:
        return f'Producto: {self.product}\nProveedor: {self.supplier}'