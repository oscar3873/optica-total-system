from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from .managers import UserManager
from core.models import Person

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
    imagen = models.ImageField(upload_to='profile/', null=True, blank=True, verbose_name='Imagen de perfil')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = UserManager()
    
    def __str__(self):
        return f"{self.get_full_name()}"
    
    def get_absolute_url(self):
        employee = self.employee_type
        return reverse('employees_app:profile_employee', kwargs={'pk': employee.pk})

