from django.db import models

from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel
from applications.clients.models import Customer
from applications.products.models import Product
from applications.core.models import BaseAbstractWithUser

# Create your models here.

class Invoice(BaseAbstractWithUser):
    """
    Clase para Facturas
        almacena faturas emitidas por la empresa
    """

    invoice_num = models.PositiveBigIntegerField(verbose_name='Numero de factura')
    invoice_type = models.CharField(max_length=20, verbose_name='Tipo de factura')
    client = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='invoice', null=True , blank=True)


class Receipt(BaseAbstractWithUser):
    """
    Clase para Recibos/Comprobantes de venta
        almacena recibos emitidos por la empresa
    """ 

    # receipt_type = models.CharField(max_length=20, verbose_name='Tipo de recibo')
    client = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='receipt', null=True , blank=True)
    sale_num = models.IntegerField()
    total = models.PositiveIntegerField()


class Sale(BaseAbstractWithUser):
    """
    Clase para venta
        almacena los datos necesarios para una venta realizada con estados de la misma
            -state: estado de la venta (predeterminado 'PENDIENTE' -al instanciar-)
            -invoice: factura correspondiente a la venta a realizar
            -customer (opcional): cliente asociado a la venta
            -total: total de los items a vender
            -refund_date (posibles casos): fecha de devolucion 
    """

    STATE = [
        ('COMPLETADO','COMPLETADO'),
        ('PENDIENTE','PENDIENTE'),
        ('DEVOLUCION','DEVOLUCION'),
        ('CANCELADO','CANCELADO')
    ]

    state = models.CharField(max_length=10, choices=STATE, default='PENDIENTE', blank=False, null=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='sales', null=True, blank=True)
    receipt = models.ForeignKey(Receipt, on_delete=models.PROTECT, related_name='sales', null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sales', null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    refund_date = models.DateTimeField(verbose_name='Fecha de devolucion', null=True, blank=True)


# class PaymentMethod_Sale(BaseAbstractWithUser):
#     """
#     Clase interemedia de Metodos de pago y Ventas
#         (-sale, -payment): almacena las PK de Metodo de pago y de la Venta
#         -amount: monto del metodo de pago
#     """
#     sale = models.ForeignKey(Sale, on_delete=models.PROTECT, related_name='paymentmethod_sale')
#     payment = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, related_name='paymentmethod_sale')
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self) -> str:
#         return f'Venta: {self.sale}\n{self.payment}\nMonto: {self.amount}'


class OrderDetail(BaseAbstractWithUser):
    """
    Clase de Detalles de Venta
        -product: prodcuto asociado a la venta
        -sale: orde de venta
        -quantity: cantidad solicitada del producto
        -price: costo total (precio * cantidad)
    """
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_detaill', null=True, verbose_name='Producto')
    sell = models.ForeignKey(Sale, on_delete=models.PROTECT, related_name='order_detaill', null=True, verbose_name='Venta')
    quantity = models.IntegerField(blank=False, null=False, verbose_name='Cantidad')
    price = models.FloatField(null=False, blank=False, verbose_name='Subtotal')

    def __str__(self) -> str:
        return (f'Orden de venta: {self.sell}\n' +
                f'Producto: {self.product}\n' +
                f'Cantidad: {self.quantity}\n' +
                f'Total: $ {self.product.sale_price * self.quantity}'
                )