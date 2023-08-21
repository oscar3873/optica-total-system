from django.db import models

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    phone_number = models.IntegerField(verbose_name='Telefono de contacto')
    email = models.EmailField(verbose_name='Correo electronico', null=True, blank=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self) -> str:
        return f'{self.name} | {self.phone_number} | {self.email}'