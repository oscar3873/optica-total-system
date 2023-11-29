from datetime import timezone
from django.db import models
from core.managers import BaseManager

class BranchManager(BaseManager):
    """
    Manager para Sucursales
    """
    def all(self):
        return self.filter(deleted_at=None)
    
class ObjectiveActiveBranchManager(models.Manager):
    def active_branch_objectives(self):
        current_date = timezone.now().date()
        return self.filter(
            objetive__start_date__lte=current_date,
            objetive__exp_date__gte=current_date
        )