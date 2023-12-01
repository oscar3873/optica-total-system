
from core.managers import BaseManager
from django.utils import timezone

class PaymentManager(BaseManager):
    def all(self):
        return self.filter(deleted_at=None).order_by('created_at')
