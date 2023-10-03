from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

class CashRegisterManager(models.Manager):
    def create_cash_register(self, initial_balance, branch, user_made, currency, final_balance):
        cash_register = self.create(
            initial_balance = initial_balance, 
            branch = branch, 
            user_made = user_made, 
            date_open=timezone.now(), 
            currency = currency,
            final_balance = final_balance
        )
        return cash_register
    
    #Esto todavia no tenerlo en cuenta esta sin revizar
    def get_final_balance(self, cash_register):
        movements = cash_register.movements.all()
        income = movements.filter(type_operation='in').aggregate(total=models.Sum('amount'))['total'] or 0
        expenses = movements.filter(type_operation='out').aggregate(total=models.Sum('amount'))['total'] or 0
        final_balance = income - expenses
        return final_balance
        

class CashRegisterDetailManager(models.Manager):
    def registered_amount_for_type_method(self, type_method, movements_model, cashregister):
        """
        Esta funcion debe devolver lo que hay registrado en la caja del sistema segun metodo de pago
        Los metodos son (Efectivo, Tarjeta de Credito, Tarjeta de Debito, Transferencia)
        de la tabla CashRegisterDetail type_method es el tipo <PaymentType>
        
        Recordar que el monto de la caja se calcula teniendo en cuenta los movimientos registrados
        
        """
        
        #Se recuperan todos los movimientos en la caja
        movements = movements_model.objects.filter(cash_register=cashregister, deleted_at=None)
        #Se filtran todos los movimientos por type_method
        movements = movements.filter(payment_method=type_method)
        #Se recupera el balanca inicial de la caja (Caso efectivo)
        initial_balance_cashregister = cashregister.initial_balance or 0
        #Se recupera el total de ingresos y egresos de la caja
        total_amount_ingresos = movements.filter(type_operation='in').aggregate(total=models.Sum('amount'))['total'] or 0
        total_amount_egresos = movements.filter(type_operation='out').aggregate(total=models.Sum('amount'))['total'] or 0
        #Se calcula el total de la caja
        total_amount = total_amount_ingresos - total_amount_egresos
        
        #Se considera el caso para el efectivo porque la caja se abre en efectivo
        
        #harcodeado
        registered_amount = (total_amount + initial_balance_cashregister) if type_method.name == "Efectivo" else total_amount
        return registered_amount


class MovementManager(models.Manager):

    def _check_sufficient_funds(self, cash_register, amount):
        """
        Verifica si hay fondos suficientes en la caja.
        """
        if cash_register.final_balance < amount:
            raise ValueError(f"Not enough funds. Current balance: {cash_register.final_balance}, Amount: {amount}")

    def update_balance(self, cash_register, amount, operation):
        """
        Actualiza el balance final de la caja.
        """
        amount = abs(amount)
        
        if operation == 'in':
            cash_register.final_balance += amount
        elif operation == 'out':
            # Antes de realizar una operación de salida, verificamos los fondos.
            self._check_sufficient_funds(cash_register, amount)
            cash_register.final_balance -= amount
        else:
            raise ValueError(f"Invalid operation: {operation}")
        cash_register.save()
        
    def update_balance_reverse(self, cash_register, amount, operation, current_movement):
        """
        Actualiza el balance de una caja activa.
        current_movement es el objeto (movimiento) actual antes de ser modificado
        """
        amount = abs(amount)
        current_amount = abs(current_movement.amount)
        current_operation = current_movement.type_operation
        
        # Revierte el movimiento anterior
        self.update_balance(cash_register, current_amount, 'in' if current_operation == 'out' else 'out')
        
        try:
            # Aplica el nuevo movimiento
            self.update_balance(cash_register, amount, operation)
        except ValueError as e:
            # Si ocurre un error, significa que estoy tratando de retirar un monto que no tengo, por lo que debo eliminar el movimiento
            current_movement.delete()
            raise e


"""
class Transaction(BaseAbstractWithUser):
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, null=True, blank=True)
    date_transaction = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
"""
"""
    def form_valid(self, form):
        branch = self.request.user.branch
        cash_register = CashRegister.objects.get(branch=branch, is_close=False)
        
        try:
            Movement.objects.update_balance(cash_register, form.instance.amount, form.instance.type_operation)
            form.instance.amount = abs(form.instance.amount)
            form.instance.date_movement = timezone.now()
            form.instance.cash_register = cash_register
            form.instance.currency = cash_register.currency
            form.instance.user_made = self.request.user
            form.save()
            Transaction.objects.create_transaction(form.instance)
"""