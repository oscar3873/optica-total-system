from django.db import models

from applications.core.models import Person
from applications.users.models import User


# Create your models here.

#No se usa el modelo
class Employee(Person):
    pass
"""     
    #Clase de Empleados
    #    almacenamineto de datos de empleados con sus datos generales y a que surucrsal pertenece
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employee')
    user_made = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='from_employee')
    address = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self) -> str:
        return f'{self.get_full_name()}' """
