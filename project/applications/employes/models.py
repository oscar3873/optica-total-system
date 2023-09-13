from django.db import models

from applications.core.models import Person, BaseAbstractWithUser, Objetives


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

class Employee_Objetives(BaseAbstractWithUser):
    """
    Clase intermedia para los objetivos de los empleados.
        is_completed: Indicador de Objetivo completado o no.
        employee: El objetivo es compleado por un empleado, el registro es individual
        objetive: Objetivo para empleados
        accumulated: Cantidad acumulada del objetivo ("Porcentaje")
    """
    is_completed = models.BooleanField(default=False, null=True, blank=True, verbose_name='Completado')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Empleado')
    objetive = models.ForeignKey(Objetives, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Objetivo')
    accumulated = models.PositiveIntegerField(default= 0, null=True, blank=True, verbose_name='Acumulado')