from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Objetives
from applications.branches.models import Branch, Branch_Objetives
from applications.employes.models import Employee, Employee_Objetives
from project.settings.base import DATE_NOW

@receiver(post_save, sender=Objetives)
def create_objective_receiver(sender, instance, created, **kwargs):
    if created:
        if instance.to == "EMPLEADO":
            employees = Employee.objects.all()
            for employee in employees:
                Employee_Objetives.objects.create(
                    employee=employee,
                    objective=instance
                )
        elif instance.to == "SUCURSAL":
            branches = Branch.objects.all()
            for branch in branches:
                Branch_Objetives.objects.create(
                    branch=branch,
                    objective=instance
                )

@receiver(post_save, sender=Objetives)
def update_objective_receiver(sender, instance, **kwargs):
    if instance.exp_date <= DATE_NOW.date():
        if instance.to == "EMPLEADO":
            employees = Employee.objects.all()
            for employee in employees:
                objective = employee.employee_objetives.get(objective=instance)
                if objective.accumulated >= instance.quantity:
                    objective.is_completed = True
                    objective.save()
        elif instance.to == "SUCURSAL":
            branches = Branch.objects.all()
            for branch in branches:
                objective = branch.branch_objetives.get(objective=instance)
                if objective.accumulated >= instance.quantity:
                    objective.is_completed = True
                    objective.save()
