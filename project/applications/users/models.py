from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from applications.core.models import Person

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

    role = models.CharField(max_length=15, choices=ROLE, default='EMPLEADO', null=True, blank=True,verbose_name="rol")
    username = models.CharField(max_length=50, unique=True,verbose_name="Nombre de usuario")
    # branch = models.ForeignKey(Branch, on_delete=models.PROTECT, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = UserManager()

    
    def __str__(self):
        return f"{self.get_full_name()}"
