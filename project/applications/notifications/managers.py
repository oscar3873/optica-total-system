from applications.core.managers import BaseManager

class NotificationsManager(BaseManager):
    """
    Manager para Notifications
    """
    def all(self):
        return self.filter(deleted_at=None)