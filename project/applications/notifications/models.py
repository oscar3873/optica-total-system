from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from applications.core.models import BaseAbstractWithUser
# Create your models here.
class Notifications(BaseAbstractWithUser):
    details = models.TextField()  # Detalles específicos de la acción
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self) -> str:
        return f'{self.content_object}'