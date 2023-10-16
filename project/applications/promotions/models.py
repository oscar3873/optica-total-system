from django.db import models

from applications.core.models import BaseAbstractWithUser
from applications.products.models import Product
from applications.branches.models import Branch

# Create your models here.
class Promotion(BaseAbstractWithUser): # promocion de 2 products
    """
    Clase para Promociones
        guarda datos generales de una promocion
    """

    PROMOTION = [
        ('A', '2x1'),
        ('B', '-50% 2da unidad'),
        ('C', 'DESCUENTO %'),
    ]

    name = models.CharField(max_length=100, verbose_name='Nombre', null=True, blank=True) # Promo "Verano", "Friday", "Hotsale"
    type_discount = models.CharField(max_length=15, choices=PROMOTION, default=PROMOTION[2], verbose_name='Tipo de promocion', null=True, blank=True)
    description = models.TextField(verbose_name='Descripcion', null=True, blank=True)
    start_date = models.DateField(verbose_name='Inicio', null=True, blank=True)
    end_date = models.DateField(verbose_name='Fin', null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Descuento")
    productA = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="promotion_product_A", null=True, blank=True, verbose_name='Producto')
    productB = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="promotion_product_B", null=True, blank=True, verbose_name='Producto')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Sucursal')

    def __str__(self) -> str:
        return f'{self.name}\n{self.description}\nDescuento: {self.discount}%'