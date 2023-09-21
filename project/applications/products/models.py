from django.db import models

from applications.core.models import BaseAbstractWithUser
from applications.branches.models import Branch
from .managers import *

# Create your models here.
class Category(BaseAbstractWithUser):
    """
    Clase para Categorias
    """
    name = models.CharField(max_length=100, blank=False, null=True,verbose_name='nombre de la Categoria')

    def __str__(self) -> str:
        return f'{self.name}'


class Brand(BaseAbstractWithUser):
    """
    Clase para Marcas
    """
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self) -> str:
        return f'{self.name}'


class Product(BaseAbstractWithUser):
    """
    Clase para Productos
        almacena datos necesarios para el manejo de productos
            
    """
<<<<<<< HEAD
    name = models.CharField(max_length=50, blank=False, null=False,verbose_name="Nombre del Producto")
=======
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name="Nombre")
>>>>>>> faf6548ece2df49b8660d72f83cfb2c243f3ac0e
    barcode = models.PositiveBigIntegerField(verbose_name='Codigo de barra', null=True)
    cost_price =models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Precio de costo")
    suggested_price =models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Precio sugerido")
    sale_price =models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Precio de venta")
<<<<<<< HEAD
    description = models.CharField(max_length=250,verbose_name="Descripción")
    stock = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name='product_category',verbose_name="Categoria")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, null=True, blank=True, related_name='product_brand',verbose_name="Marca")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, null=True, blank=True, related_name='product_branch',verbose_name="Sucursal")
=======
    description = models.CharField(max_length=250, verbose_name="Descripcion")
    stock = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name='product_category', verbose_name="Categoria")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, null=True, blank=True, related_name='product_brand')
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, null=True, blank=True, related_name='product_branch')
>>>>>>> faf6548ece2df49b8660d72f83cfb2c243f3ac0e

    objects = ProductManager()

    def __str__(self) -> str:
        return (f'{self.name} - '+
                f'{self.brand} - '+
                f'{self.category} - '+
                f'Stock: {self.stock}'
                ) 


class Feature_type(BaseAbstractWithUser):
    """
    Clase del tipo de Carateristicas de una categoria para el producto 
    """
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Nombre')

    objects = FeatureTypeManager()

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name = 'Tipo Caracteristica'
        verbose_name_plural = 'Tipos Caracteristicas'


class Feature(BaseAbstractWithUser):
    """
    Clase para las caracteristicas nuevas de productos
    """
    value = models.CharField(max_length=100, blank=True, null=True, verbose_name='Valor')
    type = models.ForeignKey(Feature_type, on_delete=models.PROTECT, related_name='feature', verbose_name='Tipo de caracteristica')

    objects = FeatureManager()

    def __str__(self) -> str:
        return f'{self.type} - {self.value}'
    
    class Meta:
        verbose_name = 'Caracteristica'
        verbose_name_plural = 'Caracteristicas'

class Product_feature(BaseAbstractWithUser):
    """
    Clase Intermedia para las caracteristicas nuevas del producto
    """
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_feature', verbose_name='Producto')
    feature = models.ForeignKey(Feature, on_delete=models.PROTECT, related_name='product_feature', verbose_name='Caracteristica')

    def __str__(self) -> str:
        return f'Producto: {self.product} | Caracteristica: {self.feature}'
    
    class Meta:
        verbose_name = 'Producto x Caracteristica'
        verbose_name_plural = 'Producto x Caracteristica'