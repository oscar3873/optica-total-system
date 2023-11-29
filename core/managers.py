from django.db import models

class BaseManager(models.Manager):
    def all(self):
        return self.filter(deleted_at=None)