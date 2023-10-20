from django.db import models
from django.utils import timezone


from applications.core.models import BaseAbstractWithUser
from applications.products.models import Product
from applications.branches.models import Branch

# Create your models here.
class TypePromotion(BaseAbstractWithUser):
    name = models.CharField(max_length=100, verbose_name='Tipo de Promoción')

    def str(self):
        return self.name

class Promotion(models.Model):
    """
    Clase para Promociones
    Guarda datos generales de una promoción.
    """

    name = models.CharField(max_length=100, verbose_name='Nombre de la Promoción', null=True, blank=True)
    type_prom = models.ForeignKey(TypePromotion, on_delete=models.CASCADE, verbose_name='Tipo de promoción', null=True, blank=True)
    description = models.CharField(max_length=250, verbose_name='Descripción', null=True, blank=True)
    start_date = models.DateField(verbose_name='Inicio', null=True, blank=True)
    end_date = models.DateField(verbose_name='Fin', null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0, verbose_name="Descuento")
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Sucursal')

    def str(self):
        return f'{self.name}\n{self.description}\nDescuento: {self.discount}%'

    

class PromotionProduct(BaseAbstractWithUser):
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='promotion_products', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='promotions', null=True, blank=True)

    def str(self):
        return f'{self.promotion.name} - {self.product.name}'