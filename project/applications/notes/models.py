from django.db import models
from applications.core.models import BaseAbstractWithUser
from applications.branches.models import Branch

# Create your models here.
class Label(BaseAbstractWithUser):
    """
    Clase para añadir etiquetas de colores a las notas.
        -label: Nombre de la etiqueta.
        -color: Color de la etiqueta (hexadecimal).
    """
    label = models.CharField(max_length=20)
    color = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.label} - {self.color}'


class Note(BaseAbstractWithUser):
    """
    Clase para Notas para dejar un mensaje de algun instructivo
        -subject: Asunto de la nota
        -description: mensaje que se quiere mostrar a los usuarios del sistema
        -branch: el mensaje es para una sucursal especificao o varias
        -user: emisor de la nota
    """
    subject = models.CharField(max_length=20, blank=False, null=True, verbose_name='Asunto')
    description = models.TextField(max_length=150, blank=False, null=False, verbose_name='Mensaje')
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Sucursal')
    label = models.ForeignKey(Label, on_delete=models.SET_NULL, verbose_name='Label', null=True)

    def __str__(self) -> str:
        return (f'Asunto: {self.subject}\n'+
                f'Mensaje: {self.description}\n'+
                f'Por: {self.user_made} - Sucursal: {self.branch}'
                )
