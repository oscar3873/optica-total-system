from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee

############### CONSULTAR SI RELAMENTE ES NECESARIO YA QUE ESTA LA VIEW  ###############
# @receiver(post_save, sender=Employee)
# def set_employee_role(sender, instance, created, **kwargs):
#     if created:
#         instance.user.role = 'EMPLEADO'
#         instance.user.save()

# # Registrar la señal
# post_save.connect(set_employee_role, sender=Employee, dispatch_uid='set_employee_role')
