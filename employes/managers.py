from django.contrib.auth.models import BaseUserManager

from core.models import Objetives
from project.settings import DATE_NOW

class EmployeeManager(BaseUserManager):
    def get_employees_branch(self, branch):
        return self.filter(user__branch=branch, deleted_at=None)
    

class Employee_ObjetivesManager(BaseUserManager):
    def pre_set_data_objetives(self, employee, branch):
        objetives_active = Objetives.objects.filter(branch=branch, exp_date__gte=DATE_NOW.date(), deleted_at=None, to="EMPLEADOS")
        for objetive in objetives_active:
            employee.employee_objetives.create(
                objetive = objetive,
            )