from django.db import models

from .managers import EmployeeManager
from applications.core.models import BaseAbstractWithUser, Objetives
from applications.users.models import User

# Create your models here.

#No se usa el modelo
class Employee(models.Model):
    """No se puede hacer uso del softDelete"""
    """
    Clase de Empleados.
        -user: con todos los datos basicos de persona y a la sucursal que pertenece.
        -user_made: usuario responsable de dar el alta la cuenta.
        -employment_date: fecha del alta de relacion de dependencia.
    """
    objects = EmployeeManager()
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employee')
    user_made = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employees')
    employment_date = models.DateField(verbose_name='Fecha de contratación', null=True, blank=True)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self) -> str:
        return f'{self.user.get_full_name()}'


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