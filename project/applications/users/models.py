from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

from applications.core.models import Person
from applications.branches.models import Branch

class User(Person, AbstractUser):
    """
    Clase de Usuarios del sistema.
        -user: con todos los datos basicos de persona y a la sucursal que pertenece.
        -role: etiqueta para distinguir entre admins y empleados (o en su defecto is_staff).
        -username: 
    """
    ROLE = [
        ('ADMINISTRADOR', 'ADMINISTRADOR'),
        ('EMPLEADO', 'EMPLEADO')
    ]

    role = models.CharField(max_length=15, choices=ROLE, default='EMPLEADO', null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    # branch = models.ForeignKey(Branch, on_delete=models.PROTECT, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = UserManager()

    
    def __str__(self):
        return f"{self.get_full_name()}"


class Employee(models.Model):
    """
    Clase de Empleados.
        -user: con todos los datos basicos de persona y a la sucursal que pertenece.
        -user_made: usuario responsable de dar el alta la cuenta.
        -employment_date: fecha del alta de relacion de dependencia.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employe')
    user_made = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employees')
    employment_date = models.DateField(verbose_name='Fecha de contratación', null=True, blank=True)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self) -> str:
        return f'{self.user.get_full_name()}'
