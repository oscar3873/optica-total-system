from django.db import models
from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel


from applications.core.models import BaseAbstractWithUser

from .managers import ProductManager

# Create your models here.
class Category(BaseAbstractWithUser):
    """
    Clase para Categorias
    """
    name = models.CharField(max_length=100, blank=False, null=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Brand(BaseAbstractWithUser):
    """
    Clase para Marcas
    """
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self) -> str:
        return f'Marca: {self.name}'


class Product(BaseAbstractWithUser):
    """
    Clase para Productos
        almacena datos necesarios para el manejo de productos
            
    """
    name = models.CharField(max_length=50, blank=False, null=False)
    barcode = models.PositiveBigIntegerField(verbose_name='Codigo de barra', null=True)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=250)
    stock = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name='product_category')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, null=True, blank=True, related_name='product_brand')

    objects = ProductManager()

    def __str__(self) -> str:
        return (f'{self.name} - '+
                f'{self.brand} - '+
                f'{self.category} - '+
                f'Precio: {self.price} - '+ 
                f'Stock: {self.stock}'
                )


class Feature_type(BaseAbstractWithUser):
    """
    Clase del tipo de Carateristicas de una categoria para el producto 
    """
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Nombre')

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

    def __str__(self) -> str:
        return f'Tipo: {self.type} - Valor: {self.value}'
    
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
        verbose_name = 'Producto x Categoria'
        verbose_name_plural = 'Producto x Categoria'

# class Type_discount(BaseAbstractWithUser):
#     """
#     Clase para Tipo de Descuentos
#     """
#     name = models.CharField(max_length=50, blank=False, null=False)


# class Discount(BaseAbstractWithUser):
#     """
#     Clase para Descuentos para productos
#         -type: tipo de descuento (procentaje o monto)
#         -value: valor del porcentaje o monto
#     """
#     type = models.ForeignKey(Type_discount, on_delete=models.PROTECT)
#     value = models.FloatField()

#     def __str__(self) -> str:
#         return f'Tipo: {self.type}\nValor: {self.value}'


# class Promotion(BaseAbstractWithUser):
#     """
#     Clase para la Promocion
#         almacena datos necesarios para proveer promociones a clientes
#             -is_active: para saber si la promocion esta activa, el booleano se pone en positivo si la fecha actual esta entre start_date y end_date
#             start_date: fecha de comienzo de la promocion
#             end_date: fecha de finalizacion de la promocion
#     """
#     is_active = models.BooleanField(default=False)
#     name = models.CharField(max_length=20, blank=True, null=False)
#     description = models.CharField(max_length=50, blank=False, null=False)
#     start_date = models.DateField(null=False, blank=False)
#     end_date = models.DateField(null=False, blank=False)

#     def __str__(self) -> str:
#         return f'{self.name}\n{self.description}\Validez: {self.start_date} - {self.end_date}'
    

# class Discount_Product(BaseAbstractWithUser):
#     """
#     Clase intermedia de Descuento y Producto
#         almacena las PK del Descuento, del Producto y de la Promocion
#     """
#     product = models.ForeignKey(Product, on_delete=models.PROTECT)
#     discount = models.ForeignKey(Discount, on_delete=models.PROTECT)
#     promotion = models.ForeignKey(Promotion, on_delete=models.PROTECT)
