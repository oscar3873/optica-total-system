from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from core.models import BaseAbstractWithUser
from branches.models import Branch
from cashregister.managers import CashRegisterManager, MovementManager, CashRegisterDetailManager
from sales.models import PaymentType



class Currency(BaseAbstractWithUser):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class CashRegister(BaseAbstractWithUser):
    """Caja registradora

        Atributos:
            date_open: Fecha de apertura de la caja
            date_close: Fecha de cierre de la caja
            initial_balance: Saldo inicial de la caja
            final_balance: Saldo final de la caja de sistema
            counted_balance: Saldo contado de la caja fisica
            difference: Faltante de la caja fisica ( difference + counted_balance = final_balance)
            branch: Sucursal a la que pertenece la caja
            currency: Moneda a la que pertenece la caja
            is_close: Indica si la caja esta cerrada
    """
    date_open = models.DateTimeField(auto_now_add=True, verbose_name="Fecha apertura")
    date_close = models.DateTimeField(null=True, blank=True, verbose_name="Fecha cierre")
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto inicial")
    final_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Monto final")
    counted_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Monto de la caja fisica")
    difference = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Diferencia")
    observations = models.TextField(null=True, blank=True, verbose_name="Observaciones")
    branch = models.ForeignKey('branches.Branch', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Sucursal")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Divisa")
    is_close = models.BooleanField(default=False, verbose_name="Estado")
    
    objects = CashRegisterManager()
    
    def __str__(self):
        return "Caja #" + str(self.pk) + " - " + str(self.date_open.__format__('%d/%m/%Y'))


class CashRegisterDetail(BaseAbstractWithUser):
    cash_register = models.ForeignKey(CashRegister, on_delete=models.CASCADE, null=True, blank=True)
    type_method = models.ForeignKey(PaymentType, on_delete=models.CASCADE, null=True, blank=True)
    registered_amount = models.DecimalField(max_digits=10, decimal_places=2)
    counted_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    difference = models.DecimalField(max_digits=10, decimal_places=2)
    
    objects = CashRegisterDetailManager()


class TransactionType(BaseAbstractWithUser):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    


class Transaction(BaseAbstractWithUser):
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, null=True, blank=True)
    date_transaction = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    branch = models.ForeignKey('branches.Branch', on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')


class Movement(BaseAbstractWithUser):
    TYPE_OPERATION = [
        ('Ingreso', 'Ingreso'),
        ('Egreso', 'Egreso')
    ]
    
    date_movement = models.DateField(auto_now_add=True, verbose_name="Fecha")
    cash_register = models.ForeignKey(CashRegister, on_delete=models.CASCADE, verbose_name="Caja")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name="Descripción")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name="Moneda")
    type_operation = models.CharField(max_length=50, choices=TYPE_OPERATION, verbose_name="Operacion")
    payment_method = models.ForeignKey(PaymentType, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Metodo de pago")
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Transacción")
    withdrawal_reason = models.CharField(max_length=100, null=True, blank=True, help_text="Campo para ingresar el motivo de devolucion", verbose_name="Razon de devolución")
    
    objects = MovementManager()
    
    def __str__(self):
        return str(self.type_operation) + ' ' + str(self.amount) + ' ' + ' por ' + str(self.user_made)
