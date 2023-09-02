from applications.core.managers import BaseManager


class NotasManager(BaseManager):
    """
    Manager para Notas
    """
    def all(self):
        return self.filter(deleted_at=None)