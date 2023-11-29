from collections import defaultdict
from django.db import models
from django.db.models.functions import Trunc
from django.utils import timezone


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

    def get_movements_data(self, cashregister):
        return cashregister.movement_set.all().filter(deleted_at=None)
    
    #Esto todavia no tenerlo en cuenta esta sin revizar
    def get_archering_data(self, cash_register):
        from cashregister.models import CashRegisterDetail, PaymentType
        from users.models import User

        arqueos = CashRegisterDetail.objects.filter(cash_register=cash_register)
        arqueos = arqueos.annotate(creation_datetime=Trunc('created_at', 'minute'))
        resultados = arqueos.values(
            'creation_datetime', 'cash_register', 'type_method', 'registered_amount', 'counted_amount', 'difference', 'user_made'
        )

        # Crear un diccionario para agrupar los resultados por fecha
        data_by_datetime = defaultdict(list)
        for resultado in resultados:
            creation_datetime = resultado['creation_datetime']
            type_method_id = resultado['type_method']
            type_method_name = PaymentType.objects.get(id=type_method_id).name
            resultado['type_method'] = type_method_name  # Reemplazar el ID por el nombre
            user_made_id = resultado['user_made']
            user_made_name = User.objects.get(id=user_made_id)
            resultado['user_made'] = user_made_name  # Reemplazar el ID por el nombre
            data_by_datetime[creation_datetime].append(resultado)

        # Formatear los resultados en la estructura deseada
        formatted_results = {}
        cont = 0
        for datetime, data in data_by_datetime.items():
            formatted_result = {datetime: data}
            formatted_results[cont] = formatted_result
            cont += 1
        return formatted_results


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
        total_amount_ingresos = movements.filter(type_operation='Ingreso').aggregate(total=models.Sum('amount'))['total'] or 0
        total_amount_egresos = movements.filter(type_operation='Egreso').aggregate(total=models.Sum('amount'))['total'] or 0
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
        # print('\n\n\n\n', operation)
        if operation == 'Ingreso':
            cash_register.final_balance += amount
        elif operation == 'Egreso':
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
        self.update_balance(cash_register, current_amount, 'Ingreso' if current_operation == 'Egreso' else 'Egreso')
        
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