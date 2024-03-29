from django.db import models
from django_afip.models import Receipt 
from django.urls import reverse

from clients.models import Customer
from products.models import Product
from core.models import BaseAbstractWithUser
from .managers import PaymentManager

# Create your models here.


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

    receipt = models.OneToOneField(Receipt, on_delete=models.SET_NULL, related_name='sales', null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sales', null=True, blank=True, verbose_name='Cliente')
    state = models.CharField(max_length=10, choices=STATE, default='PENDIENTE', blank=False, null=False, verbose_name='Estado')
    refund_date = models.DateTimeField(verbose_name='Fecha de devolucion', null=True, blank=True)
    discount = models.IntegerField(verbose_name='Descuento', default=0, null=True, blank=True)
    discount_extra = models.PositiveIntegerField(verbose_name='Descuento', default=0, null=True, blank=True)
    missing_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True, verbose_name="Saldo")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, verbose_name="Subtotal")
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, verbose_name="Total")
    branch = models.ForeignKey('branches.Branch', on_delete=models.PROTECT, related_name='sales', null=True, blank=True)
    commision_user = models.ForeignKey('employes.Employee', on_delete=models.PROTECT, related_name='sales', null=True, blank=True)
    surcharge = models.PositiveIntegerField(verbose_name='Recargo', default=0, null=True, blank=True)

    def __str__(self):
        return f"COD: {self.pk} - $ {self.total}"
    
    def get_absolute_url(self):
        return reverse('sales_app:sale_detail_view', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

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
    name = models.CharField(max_length=50, verbose_name='Tipo de Pago')
    
    def __str__(self):
        return self.name
    


#ESTO VA EN LA APLICACION DE SALES
class PaymentMethod(BaseAbstractWithUser):
    name = models.CharField(max_length=50, verbose_name='Metodo de Pago')
    type_method = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + ' - ' + str(self.type_method)

#ESTO VA EN LA APLICACION DE SALES
class Payment(BaseAbstractWithUser):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='payments', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    date_payment = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True, max_length=100, default='Sin descripcion')
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT, related_name='sale_payment', null=True)
    movement = models.OneToOneField('cashregister.Movement', on_delete=models.PROTECT, related_name='mov_payment', null=True)

    objects = PaymentManager()

    def __str__(self) -> str:
        return f'Pago de Venta #{self.sale.pk}: Cliente: {self.customer} | Metodo de pago: {self.payment_method.name} | Monto: {self.amount}' 