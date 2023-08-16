from django.db import models

from django.contrib.auth.models import BaseUserManager

class PersonManager(BaseUserManager, models.Manager):
    
    def create_person_dict(self, **person_data):
        person = self.model(**person_data)
        person.save()
        return person
    
    