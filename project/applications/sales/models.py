from django.db import models

from applications.clients.models import Customer
from applications.products.models import Product
from applications.core.models import BaseAbstractWithUser
from applications.branches.models import Branch

# Create your models here.

class InvoiceType(BaseAbstractWithUser):
    TYPE = [
        ('A', 'Factura A'),
        ('B', 'Factura B'),
        ('X', 'Comprobante de pago'),
    ]

    num_invoice = models.CharField(unique=True, db_index=True, null=True, blank=True)
    name = models.CharField(max_length=10, choices=TYPE, default=TYPE[0], null=True, blank=True)

class Invoice(BaseAbstractWithUser):
    """
    Clase para Facturas
        almacena faturas emitidas por la empresa
    """

    invoice_num = models.PositiveBigIntegerField(verbose_name='Numero de factura')
    invoice_type = models.ForeignKey(InvoiceType, on_delete=models.SET_NULL, verbose_name='Tipo de factura', null=True , blank=True)
    client = models.ForeignKey(Customer, on_delete=models.SET_NULL, related_name='invoice', null=True , blank=True)


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

    date_time_sale = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='sales', null=True, blank=True)
    receipt = models.ForeignKey(Receipt, on_delete=models.PROTECT, related_name='sales', null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sales', null=True, blank=True, verbose_name='Cliente')
    state = models.CharField(max_length=10, choices=STATE, default='PENDIENTE', blank=False, null=False, verbose_name='Estado')
    refund_date = models.DateTimeField(verbose_name='Fecha de devolucion', null=True, blank=True)
    discount = models.PositiveIntegerField(verbose_name='Descuento',  null=True, blank=True)
    missing_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True, verbose_name="Saldo")
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, verbose_name="Total")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='sales', null=True, blank=True)

class OrderDetail(BaseAbstractWithUser):
    """
    Clase de Detalles de Venta
        -product: prodcuto asociado a la venta
        -sale: orde de venta
        -quantity: cantidad solicitada del producto
        -price: costo total (precio * cantidad)
    """
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_detaill', null=True, verbose_name='Producto')
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT, related_name='order_detaill', null=True, verbose_name='Venta')
    quantity = models.IntegerField(blank=False, null=False, verbose_name='Cantidad')
    price = models.FloatField(null=False, blank=False, verbose_name='Subtotal')
    discount = models.FloatField(verbose_name='Descuento', blank=True, null=True)

    def __str__(self) -> str:
        return (f'Orden de venta: {self.sale}\n' +
                f'Producto: {self.product}\n' +
                f'Cantidad: {self.quantity}\n' +
                f'Total: $ {self.product.sale_price * self.quantity}'
                )



class PaymentType(BaseAbstractWithUser):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    


#ESTO VA EN LA APLICACION DE SALES
class PaymentMethod(BaseAbstractWithUser):
    name = models.CharField(max_length=50)
    type_method = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + ' - ' + str(self.type_method)

#ESTO VA EN LA APLICACION DE SALES
class Payment(BaseAbstractWithUser):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    date_payment = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True, max_length=100, default='Sin descripcion')
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT, related_name='sale_payment', null=True)
