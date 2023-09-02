from django.db import models
from django.utils import timezone

class CashRegisterManager(models.Manager):
    def create_cash_register(self, initial_balance, branch, user_made, currency):
        cash_register = self.create(initial_balance=initial_balance, branch=branch, user_made=user_made, date_open=timezone.now(), currency=currency)
        return cash_register
    
    def get_final_balance(self, cash_register):
        movements = cash_register.movements.all()
        income = movements.filter(type_operation='in').aggregate(total=models.Sum('amount'))['total'] or 0
        expenses = movements.filter(type_operation='out').aggregate(total=models.Sum('amount'))['total'] or 0
        final_balance = income - expenses
        return final_balance
        

class CashRegisterDetailManager(models.Manager):
    def get_registered_amount(self, cash_register, type_method_payment):
        from .models import Movement

        movements = Movement.objects.filter(cash_register=cash_register, payment_method__type_method=type_method_payment)
        return movements.aggregate(total=models.Sum('amount'))['total'] or 0

