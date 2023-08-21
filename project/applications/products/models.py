from django.db import models
from applications.suppliers.models import Supplier
from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel


# Create your models here.
class Category(SoftDeletionModel, TimestampsModel):
    """
    Clase para Categorias
    """
    name = models.CharField(max_length=100, blank=False, null=True)

    def __str__(self) -> str:
        return f'Categoria: {self.name}'


class Brand(SoftDeletionModel, TimestampsModel):
    """
    Clase para Marcas
    """
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self) -> str:
        return f'Marca: {self.name}'

class Product(SoftDeletionModel, TimestampsModel):
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
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True, blank=True, related_name='product_supplier')

    def __str__(self) -> str:
        return (f'Nombre: {self.name}\n'+
                f'{self.brand}\n'+
                f'{self.category}\n'+
                f'Codigo: {self.barcode}\n'+
                f'Precio: {self.price}\n'+ 
                f'Stock: {self.stock}\n'+
                f'Descripcion: {self.description}'
                )


class Product_Supplier(SoftDeletionModel, TimestampsModel):
    """
    Clase intermedia de Producto y Proveedor almacenando sus PK para sus posteriores analisis
    """
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_suppliers', null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='product_suppliers', null=True)

    def __str__(self) -> str:
        return f'Producto: {self.product}\nProveedor: {self.supplier}'


# class Type_discount(SoftDeletionModel, TimestampsModel):
#     """
#     Clase para Tipo de Descuentos
#     """
#     name = models.CharField(max_length=50, blank=False, null=False)


# class Discount(SoftDeletionModel, TimestampsModel):
#     """
#     Clase para Descuentos para productos
#         -type: tipo de descuento (procentaje o monto)
#         -value: valor del porcentaje o monto
#     """
#     type = models.ForeignKey(Type_discount, on_delete=models.PROTECT)
#     value = models.FloatField()

#     def __str__(self) -> str:
#         return f'Tipo: {self.type}\nValor: {self.value}'


# class Promotion(SoftDeletionModel, TimestampsModel):
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
    

# class Discount_Product(SoftDeletionModel, TimestampsModel):
#     """
#     Clase intermedia de Descuento y Producto
#         almacena las PK del Descuento, del Producto y de la Promocion
#     """
#     product = models.ForeignKey(Product, on_delete=models.PROTECT)
#     discount = models.ForeignKey(Discount, on_delete=models.PROTECT)
#     promotion = models.ForeignKey(Promotion, on_delete=models.PROTECT)
