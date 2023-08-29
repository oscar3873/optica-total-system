from django.db import models

# Create your models here.
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
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, verbose_name='Sucursal')

    def __str__(self) -> str:
        return (f'Asunto: {self.subject}\n'+
                f'Mensaje: {self.description}\n'+
                f'Por: {self.user_made} - Sucursal: {self.branch}'
                ) 
