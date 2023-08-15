from django.db import models

from django.contrib.auth.models import BaseUserManager

class PersonManager(BaseUserManager, models.Manager):

    def create_person(self, name, lastname, birth_date, dni, phone_number=None, email=None, **extra_fields):
        person = self.model(
            name = name,
            lastname = lastname,
            phone_number = phone_number,
            dni = dni,
            email = email,
            birth_date = birth_date,
            **extra_fields
        )
        person.save()
        return person
    
    def create_person_dict(self, **person_data):
        person = self.model(**person_data)
        person.save()
        return person
    
    