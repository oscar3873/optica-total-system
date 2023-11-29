from django.db.models.signals import post_save
from django.db.models import Sum

from sales.models import Sale

from .models import Objetives
from branches.models import Branch_Objetives
from employes.models import Employee, Employee_Objetives

def create_objective_receiver(instance, created, **kwargs):
    if created:
        if instance.to == "EMPLEADOS":
            employees = Employee.objects.filter(user__branch=instance.branch)
            for employee in employees:
                sales = employee.user.sale_set.filter(created_at__date__range=(instance.start_date, instance.exp_date))
                total_ventas = sales.aggregate(total=Sum('total'))
                
                Employee_Objetives.objects.create(
                    employee=employee,
                    objetive=instance,
                    accumulated = total_ventas['total'] or 0
                )

        elif instance.to == "SUCURSAL":
            branch = instance.branch
            total_accumulated = Sale.objects.filter(
                    user_made__is_staff=False,
                    branch=branch,
                    created_at__date__range=(instance.start_date, instance.exp_date),
                    state="COMPLETADO"
                ).aggregate(total=Sum('total'))
            
            Branch_Objetives.objects.create(
                branch = branch,
                objetive = instance,
                accumulated = total_accumulated['total'] or 0
            )
post_save.connect(create_objective_receiver, sender=Objetives)
