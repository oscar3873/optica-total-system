
from applications.core.managers import BaseManager
from project.settings.base import DATE_NOW

class PaymentManager(BaseManager):
    def all(self):
        return self.filter(deleted_at=None).order_by('created_at')
