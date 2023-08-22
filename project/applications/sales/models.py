from django.db import models
from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel

from applications.clients.models import Customer
from applications.products.models import Product
from applications.employes.models import Employee

# Create your models here.
class PaymentMethod(SoftDeletionModel, TimestampsModel):
    """
    Clase de Metodo de pago
        instanciacion de metodos propios (efectivo, t. credito, t. debito, etc)
    """
    method = models.CharField(max_length=20)
    
    def __str__(self) -> str:
        return f'Metodo de pago: {self.method}'


class Invoice(SoftDeletionModel, TimestampsModel):
    """
    Clase para Facturas
        almacena el tipo de facturas/ticket disponibles que provee la institucion
    """

    invoice_num = models.PositiveBigIntegerField(verbose_name='Numero de factura')
    invoice_type = models.CharField(max_length=20, verbose_name='Tipo de factura')


class Sale(SoftDeletionModel, TimestampsModel):
    """
    Clase para venta
        almacena los datos necesarios para una venta realizada con estados de la misma
            -state: estado de la venta (predeterminado 'PENDIENTE' -al instanciar-)
            -employee: asesor que realiza la venta
            -invoice: factura correspondiente a la venta a realizar
            -customer (opcional): cliente asociado a la venta
            -total: total de los items a vender
            -refund_date (casos):  
    """

    STATE = [
        ('COMPLETADO','COMPLETADO'),
        ('PENDIENTE','PENDIENTE'),
        ('DEVOLUCION','DEVOLUCION'),
        ('CANCELADO','CANCELADO')
    ]

    state = models.CharField(max_length=10, choices=STATE, default='PENDIENTE', blank=False, null=False)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='sales')
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='sales')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sales', null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    refund_date = models.DateTimeField()

    def __str__(self) -> str:
        return (f'Numero de factura: {self.invoice.invoice_num}\n'+
                f'Tipo: {self.invoice.invoice_type}\n'+
                f'Asesor: {self.employee}')


class PaymentMethod_Sale(SoftDeletionModel, TimestampsModel):
    """
    Clase interemedia de Metodos de pago y Ventas
        (-sale, -payment): almacena las PK de Metodo de pago y de la Venta
        -amount: monto del metodo de pago
    """
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT, related_name='paymentmethod_sale')
    payment = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, related_name='paymentmethod_sale')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f'Venta: {self.sale}\n{self.payment}\nMonto: {self.amount}'


class OrderDetaill(SoftDeletionModel, TimestampsModel):
    """
    Clase de Detalles de Venta
        -product: prodcuto asociado a la venta
        -sale: orde de venta
        -quantity: cantidad solicitada del producto
        -price: costo total (precio * cantidad)
    """
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_detaill', null=True)
    sell = models.ForeignKey(Sale, on_delete=models.PROTECT, related_name='order_detaill', null=True)
    quantity = models.IntegerField(blank=False, null=False)
    price = models.FloatField(null=False, blank=False)

    def __str__(self) -> str:
        return (f'Orden de venta: {self.sell}\n' +
                f'Producto: {self.product}\n' +
                f'Cantidad: {self.quantity}\n' +
                f'Total: $ {self.product.price * self.quantity}'
                )