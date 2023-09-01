from applications.core.managers import BaseManager

class BranchManager(BaseManager):
    """
    Manager para Sucursales
    """
    def all(self):
        return self.filter(deleted_at=None)