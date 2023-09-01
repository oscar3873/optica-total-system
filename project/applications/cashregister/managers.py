from django.db import models
from django.utils import timezone

class CashRegisterManager(models.Manager):
        def create_cash_register(self, initial_balance, branch, user_made, currency):
            cash_register = self.create(initial_balance=initial_balance, branch=branch, user_made=user_made, date_open=timezone.now(), currency=currency)
            return cash_register
