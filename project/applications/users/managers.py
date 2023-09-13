from django.contrib.auth.models import BaseUserManager
from django.urls import reverse

class UserManager(BaseUserManager):

    def get_employees_branch(self, branch):
        #obtiene los empleados de una sucursal
        employees_per_branch = self.get_all_employeers().filter(branch=branch)
        return employees_per_branch

    def all(self):
        users = self.filter(deleted_at=None)
        return users
    def get_employee(self,pk):
        employee=self.get(pk=pk,role='EMPLEADO',is_staff=False,is_superuser=False)
        return employee
    """ Esto lo agrego Joaquin """
    def get_all_employeers(self):
        employeers = self.filter(role='EMPLEADO',is_staff=False,is_superuser=False)
        return employeers

    def _create_user(self, first_name, last_name, username, email, password, is_staff, is_superuser, role, branch=None, **extra_fields):
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            role= role,
            branch = branch,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, first_name, last_name, username, email, password, branch, **extra_fields): # Para Empleados
        is_staff = False
        is_superuser = False
        role = 'EMPLEADO'
        return self._create_user(first_name, last_name, username, email, password, is_staff, is_superuser, role, branch, **extra_fields)

    def create_superuser(self, first_name, last_name, username, email, password, branch=None, **extra_fields): # Para SuperAdmin (SALTACODE)
        is_staff = True
        is_superuser = True
        role = 'ADMINISTRADOR'
        return self._create_user(first_name, last_name, username, email, password, is_staff, is_superuser, role, branch, **extra_fields)
    
    def create_admin(self, first_name, last_name, username, email, password, branch=None, **extra_fields): # Para Admin (OPTICA-TOTAL)
        is_staff = True
        is_superuser = False
        role = 'ADMINISTRADOR'
        return self._create_user(first_name, last_name, username, email, password, is_staff, is_superuser, role, branch, **extra_fields)

    def get_absolute_url(self):
        return reverse('employees_app:profile_employee', kwargs={'pk': self.pk})

class EmployeeManager(BaseUserManager):
    def get_employees_branch(self, branch):
        return self.filter(user__branch=branch)