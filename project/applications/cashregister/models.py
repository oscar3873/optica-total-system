from django.db import models
from applications.core.models import BaseAbstractWithUser
from applications.branches.models import Branch
from applications.cashregister.managers import CashRegisterManager




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
    date_open = models.DateTimeField(auto_now_add=True)
    date_close = models.DateTimeField(null=True, blank=True)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2)
    final_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    counted_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    difference = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    is_close = models.BooleanField(default=False)
    
    objects = CashRegisterManager()
    
    def __str__(self):
        return "Caja #" + str(self.pk) + " - " + str(self.date_open.__format__('%d/%m/%Y'))


class TypeMethodePayment(BaseAbstractWithUser):
    
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    


#ESTO VA EN LA APLICACION DE SALES
class PaymentMethod(BaseAbstractWithUser):
    
    TYPE_METHOD = [
        ('cash', 'Efectivo'),
        ('debit_card', 'Tarjeta de Débito'),
        ('credit_card', 'Tarjeta de Crédito'),
        ('transfer', 'Transferencia'),
    ]
    
    name = models.CharField(max_length=50)
    type_method = models.ForeignKey(TypeMethodePayment, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + ' - ' + str(self.type_method)
    

#ESTO VA EN LA APLICACION DE SALES
class Payment(BaseAbstractWithUser):
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_payment = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True, max_length=100, default='Sin descripcion')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)


class CashRegisterDetail(BaseAbstractWithUser):
    cash_register = models.ForeignKey(CashRegister, on_delete=models.CASCADE, null=True, blank=True)
    type_method = models.ForeignKey(TypeMethodePayment, on_delete=models.CASCADE, null=True, blank=True)
    registered_amount = models.DecimalField(max_digits=10, decimal_places=2)
    counted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    difference = models.DecimalField(max_digits=10, decimal_places=2)


class TransactionType(BaseAbstractWithUser):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    


class Transaction(BaseAbstractWithUser):
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, null=True, blank=True)
    date_transaction = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    transaction_number = models.CharField(max_length=50, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    is_refund = models.BooleanField(default=False)
    original_transaction = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    refund_reason = models.CharField(max_length=100, null=True, blank=True)


class Movement(BaseAbstractWithUser):
    
    TYPE_OPERATION = [
        ('in', 'Ingreso'),
        ('out', 'Egreso')
    ]
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    date_movement = models.DateField(auto_now_add=True, verbose_name="Fecha")
    cash_register = models.ForeignKey(CashRegister, on_delete=models.CASCADE, verbose_name="Caja")
    description = models.CharField(max_length=50, null=True, blank=True, verbose_name="Descripción")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name="Moneda")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Metodo de pago")
    type_operation = models.CharField(max_length=50, choices=TYPE_OPERATION, verbose_name="Operacion")
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Transacción")
    withdrawal_reason = models.CharField(max_length=100, null=True, blank=True, help_text="Campo para ingresar el motivo de devolucion", verbose_name="Razon de devolución")
    
    def __str__(self):
        return str(self.type_operation) + ' ' + str(self.amount) + ' ' + ' por ' + str(self.user_made)