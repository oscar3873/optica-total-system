from typing import Any
from django.contrib import messages
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView, UpdateView, FormView, ListView, DeleteView
)
from django.db import models, transaction

from django.contrib.auth.mixins import LoginRequiredMixin

from applications.branches.models import Branch
from applications.core.mixins import CustomUserPassesTestMixin
from applications.users.models import User
from applications.users.forms import *
from applications.users.utils import generate_profile_img_and_assign

from .forms import EmployeeCreateForm, EmployeeUpdateForm
from .models import Employee, Employee_Objetives
from .utils import obtener_nombres_de_campos


# Create your views here.
class EmployeeCreateView(CustomUserPassesTestMixin, FormView): # CREACION DE EMPLEADOS
    template_name = "users/signup.html"
    form_class = EmployeeCreateForm
    success_url = reverse_lazy('employees_app:list_employee')    

    @transaction.atomic
    def form_valid(self, form):
        user = self.request.user
        form.cleaned_data.pop('password2')
        
        branch_actualy = self.request.session.get('branch_actualy')
        if user.is_staff and branch_actualy:
            branch = Branch.objects.get(id=branch_actualy)
        else:
            branch = self.request.user.branch

        empleado = Employee.objects.create(
            user_made = user,
            employment_date = form.cleaned_data.pop('employment_date'),
            user = User.objects.create_user(**form.cleaned_data, branch=branch) # Funcion que crea EMPLEADOS
            )
    
        if not form.cleaned_data.get('imagen'):
            generate_profile_img_and_assign(empleado.user)
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al cargar los datos. Por favor, revise los campos.')
        return super().form_invalid(form)


class EmployeeUpdateView(UpdateView):
    model = Employee
    template_name = 'employes/components/employee_update_form.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('employees_app:list_employee')

    def get_object(self, queryset=None):
        return super().get_object(queryset).user
    
    def form_valid(self, form):
        employee = form.instance
        messages.success(self.request, 'Se actualizo los datos de %s, %s con exito.''.' % (employee.last_name, employee.first_name))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al cargar los datos. Por favor, revise los campos.')
        return super().form_invalid(form)


############## UNICA VIEW DISPONIBLE PARA EL USO #############
# Perfil de empleado
class EmployeeProfileView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'employes/profile.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_actual = self.request.user
        employee_pk = self.kwargs['pk']

        context['is_self'] = True # SI ES ADMIN O EL PROPIO EMPLEADO VIENDO SU PERFIL
        context['objectives'] = context['objectives'] = Employee_Objetives.objects.filter(employee_id=employee_pk)

        if not user_actual.is_staff and user_actual.employee_type != self.get_object(): # SI ES UN EMPLEADO QUE ESTA VIENDO OTRO PERFIL
            context['is_self'] = False
        return context

    def get_object(self, queryset=None): 
        """ Obtén el valor del parámetro 'pk' de la URL, este 
        parametro, puede ser la pk de un user, comprobar que esta pk esta relacionada 
        con alguna pk de la tabla users_employee"""
        try:
            employee = Employee.objects.get(pk=self.kwargs['pk'])
        except Employee.DoesNotExist:
            employee = None
        return employee

#Listar

class EmployeeListView(LoginRequiredMixin,ListView):
    model = Employee
    template_name = 'employes/employee_list_page.html'
    context_object_name = 'employees'

    def get_queryset(self):
        branch = self.request.user.branch

        branch_actualy = self.request.session.get('branch_actualy')
        if  self.request.user.is_staff and branch_actualy:
            branch = Branch.objects.get(id=branch_actualy)
            # Si el usuario es administrador y hay una sucursal seleccionada en la sesión,        
        # En otros casos, filtra por la sucursal del usuario
        return Employee.objects.get_employees_branch(branch).filter(deleted_at=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exclude_fields_user = [
            "role",
            "phone_code",
            "dni",
            "birth_date",
            "address",
            "id",
            "deleted_at",
            "created_at", 
            "updated_at",
            "date_joined",
            "is_active",
            "is_staff",
            "password",
            "last_login",
            "username",
            "is_superuser",
            "branch",
            "imagen",
        ]
        context['table_column'] = obtener_nombres_de_campos(User, *exclude_fields_user)
        return context
    

########################### DELETE ####################################

class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employes/employee_delete_page.html'
    success_url = reverse_lazy('employees_app:list_employee')
    
    def form_valid(self, form):
        user = self.get_object().user
        user.delete()  # Realiza la eliminación suave del usuario y por consecuencia, el empleado
        return HttpResponseRedirect(self.get_success_url())

############################ Account ####################################
class AccountView(LoginRequiredMixin, UpdateView):
    template_name = 'users/user_account_page.html'
    model = User
    form_class = UserUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form2'] = UpdatePasswordForm # Agregamos el segundo formulario al contexto
        context['change_image'] = ImagenChangeForm
        return context

    def get_object(self, queryset=None):
        try:
            employee = Employee.objects.get(pk=self.kwargs['pk'])
        except Employee.DoesNotExist:
            return None
        return employee.user

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_get = self.get_object()
        
        if user_get is None:
            return render(request, 'core/error_404_page.html')
        if not user.is_staff and user != user_get:
            return render(request, 'users/denied_permission.html')
        return super().get(request, *args, **kwargs)
    
    def get_success_url(self):
        messages.success(self.request, "Se actualizaron los datos con exito.")
        return reverse_lazy('employees_app:account', kwargs={'pk': self.kwargs['pk']})


# View para validar formulario UpdatePasswordForm
class UpdatePasswordView(LoginRequiredMixin, UpdateView):
    template_name = 'employes/employee_account_page.html'
    model = User
    form_class = UpdatePasswordForm

    def form_valid(self, form):
        # Lógica para el formulario de UpdatePasswordForm (cambio de contraseña)
        # Cambia la contraseña del usuario y redirige al inicio de sesión
        if form.is_valid():
            self.object.set_password(form.cleaned_data['password'])
            self.object.save()
            messages.success(self.request, 'La contraseña se ha cambiado con exito.')
            return redirect('employees_app:account', pk=self.kwargs['pk'])
        
        messages.error(self.request, 'La contraseña actual es incorrecta.')
        return redirect('employees_app:account', pk=self.kwargs['pk'])
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error en el formulario de cambio de contraseña.')
        return redirect('employees_app:account', pk=self.kwargs['pk'])
    
    def get_object(self, queryset=None):
        employee = Employee.objects.get(pk=self.kwargs['pk'])
        return employee.user

