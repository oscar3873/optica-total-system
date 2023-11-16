
from applications.core.managers import BaseManager
from project.settings.base import DATE_NOW

class PaymentManager(BaseManager):
    def all(self, customer):
        credits = customer.payments.filter(deleted_at=None, sale__state="PENDIENTE").order_by('created_at')
        return credits
    
    def all(self):
        return self.filter(deleted_at=None).order_by('created_at')
