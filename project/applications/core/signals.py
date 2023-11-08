from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Objetives
from applications.branches.models import Branch, Branch_Objetives
from applications.employes.models import Employee, Employee_Objetives

def create_objective_receiver(instance, created, **kwargs):
    if created:
        if instance.to == "EMPLEADOS":
            employees = Employee.objects.filter(user__branch=instance.branch)
            print('\n\n\n',employees,'\n\n\n')
            for employee in employees:
                Employee_Objetives.objects.create(
                    employee=employee,
                    objetive=instance
                )
        elif instance.to == "SUCURSAL":
            branches = Branch.objects.all()
            for branch in branches:
                Branch_Objetives.objects.create(
                    branch=branch,
                    objetive=instance
                )
post_save.connect(create_objective_receiver, sender=Objetives)
