from django.db import models

from applications.core.models import SaveGeneriModel, BaseAbstractWithUser
from .managers import NotificationsManager

# Create your models here.
class Notifications(SaveGeneriModel, BaseAbstractWithUser):
    details = models.TextField()  # Detalles específicos de la acción

    objects = NotificationsManager()

    def __str__(self) -> str:
        return f'{self.content_object}'