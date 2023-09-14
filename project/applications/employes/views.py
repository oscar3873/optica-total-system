from typing import Any, Optional
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, UpdateView, FormView,ListView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


from .forms import EmployeeCreateForm
from applications.users.models import User, Employee
#from .core.utils import obtener_nombres_de_campos
from .utils import obtener_nombres_de_campos
from applications.core.mixins import CustomUserPassesTestMixin
# Create your views here.
class EmployeeCreateView(CustomUserPassesTestMixin, FormView): # CREACION DE EMPLEADOS
    template_name = "users/signup.html"
    form_class = EmployeeCreateForm
    success_url = reverse_lazy('employees_app:list_employee')    
    def form_valid(self, form):
        form.cleaned_data.pop('password2')
        Employee.objects.create(
            user_made = self.request.user,
            employment_date = form.cleaned_data.pop('employment_date'),
            user = User.objects.create_user(**form.cleaned_data) # Funcion que crea EMPLEADOS
            )
        return super().form_valid(form)



class EmployeeUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Employee
    template_name = 'users/employee_update_page.html'
    form_class = EmployeeCreateForm
    success_url = reverse_lazy('users/employee_list_page.html')
    
    def form_valid(self, form):
        form.instance.user_made = self.request.user
        return super().form_valid(form)




############## UNICA VIEW DISPONIBLE PARA EL USO #############
# Perfil de empleado
class EmployeeProfileView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'users/profile.html'
    context_object_name = 'employee'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')  # Obtén el valor del parámetro 'pk' de la URL
        try:
            employee = Employee.objects.get(pk=pk)
            #busco en la tabla user de la base de datos un usuario con pk=pk,is_staff=False,is_superuser=False,role='EMPLEADO'
        except Employee.DoesNotExist:
            #si no encuentro lo pongo en None para manejar las vistas en los templates
            employee = None
        return employee

#Listar

class EmployeeListView(LoginRequiredMixin,ListView):
    model = Employee
    template_name = 'users/employee_list_page.html'
    context_object_name = 'employees'

    def get_queryset(self):
        branch=self.request.user.branch
        if branch==None:
            return Employee.objects.all()
        return Employee.objects.get_employees_branch(branch)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        branch = self.request.user.branch
        
        exclude_fields = ["id", "deleted_at", "created_at", "updated_at"]
        exclude_fields_user = ["role","first_name","last_name","phone_number","dni","birth_date","address","id", "deleted_at", "created_at", "updated_at","date_joined","is_active","is_staff","password","last_login","username","is_superuser"]
        context['table_column'] = obtener_nombres_de_campos(Employee, *exclude_fields)
        context['table_column_user'] = obtener_nombres_de_campos(User, *exclude_fields_user)
        context['is_staff'] =self.request.user.is_staff
        return context
    

########################### DELETE ####################################

class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'users/employee_delete_page.html'
    success_url = reverse_lazy('employees_app:list_employee')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Realiza la eliminación suave
        return HttpResponseRedirect(self.get_success_url())