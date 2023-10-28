
from applications.core.managers import BaseManager
from project.settings.base import DATE_NOW

class PaymentManager(BaseManager):
    def all(self, customer):
        credits = customer.payments.filter(deleted_at=None, sale__state="PENDIENTE")
        return credits
