from audioop import reverse
from typing import Any
from django.db import models, transaction
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, UpdateView, FormView,ListView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .forms import EmployeeCreateForm,EmployeeUpdateForm
from .models import Employee

from applications.core.mixins import CustomUserPassesTestMixin
from applications.branches.models import Branch
from applications.users.models import User
from applications.users.forms import UserUpdateForm,UpdatePasswordForm
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
        
        if user.is_staff:
            branch_actualy = self.request.session.get('branch_actualy')
            branch_actualy = Branch.objects.get(id=branch_actualy)
            branch = branch_actualy
        else:
            branch = self.request.user.branch

        Employee.objects.create(
            user_made = user,
            employment_date = form.cleaned_data.pop('employment_date'),
            user = User.objects.create_user(**form.cleaned_data, branch=branch) # Funcion que crea EMPLEADOS
            )
        
        return super().form_valid(form)
    
    def form_invalid(self, form: Any) -> HttpResponse:
        messages.error(self.request, 'Hubo un error al cargar los datos. Por favor, revise los campos.')
        return super().form_invalid(form)


class EmployeeUpdateView(UpdateView):
    model = Employee
    template_name = 'employes/employee_update_page.html'
    form_class = EmployeeUpdateForm

    def form_valid(self, form):
        user_form = UserUpdateForm(self.request.POST, instance=self.object)
        if user_form.is_valid():
            user_form.save()
            form.save()
            return redirect('employees_app:list_employee')
        else:
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

    # def get_form_kwargs(self):
    #     # Obtener la instancia de Employee que se va a editar
    #     employee_instance = get_object_or_404(Employee, pk=self.kwargs['pk'])
        
    #     # Pasar la instancia al formulario como kwarg
    #     kwargs = super().get_form_kwargs()
    #     kwargs['instance'] = employee_instance
    #     return kwargs
    
    def get_object(self, queryset=None): 
        """ Obtén el valor del parámetro 'pk' de la URL, este 
        parametro, puede ser la pk de un user, comprobar que esta pk esta relacionada 
        con alguna pk de la tabla users_employee"""
        employee = super().get_object(queryset)
        return employee.user


# Probando cuenta, no me deja hacer un update de los datod de empleado

class AccountView(LoginRequiredMixin, UpdateView):
    template_name = 'employes/employee_account_page.html'
    model = User
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        employee = Employee.objects.get(pk=self.kwargs['pk'])
        return employee.user

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_get = self.get_object()

        if not user.is_staff and user != user_get:
            return render(request, 'users/denied_permission.html')
        return super().get(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('employees_app:account', kwargs={'pk': self.kwargs['pk']})

    

############## UNICA VIEW DISPONIBLE PARA EL USO #############
# Perfil de empleado
class EmployeeProfileView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'employes/profile.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_actual = self.request.user

        context['is_self'] = True # SI ES ADMIN O EL PROPIO EMPLEADO VIENDO SU PERFIL
        try:
            employee_watching = self.get_object()
        except Employee.DoesNotExist:
            employee_watching = None

        if not user_actual.is_staff and user_actual!=employee_watching: # SI ES UN EMPLEADO QUE ESTA VIENDO OTRO PERFIL
            context['is_self'] = False
        return context

    def get_object(self, queryset=None): 
        """ Obtén el valor del parámetro 'pk' de la URL, este 
        parametro, puede ser la pk de un user, comprobar que esta pk esta relacionada 
        con alguna pk de la tabla users_employee"""
        # pk = self.request.user.pk

        pk = self.kwargs.get('pk') # PK traido de la URL
        try:
            employee = Employee.objects.get(pk=pk)

            # if not self.request.user.is_staff:
            #     employee = Employee.objects.get(user_id=pk)
            # else:
            #     employee = None
            #busco en la tabla user de la base de datos un usuario con user_id=pk

        except Employee.DoesNotExist:
            #si no encuentro lo pongo en None para manejar las vistas en los templates
            employee = None
        return employee

#Listar

class EmployeeListView(LoginRequiredMixin,ListView):
    model = Employee
    template_name = 'employes/employee_list_page.html'
    context_object_name = 'employees'

    def get_queryset(self):
        branch = self.request.user.branch

        if  self.request.user.is_staff:
            branch_actualy = self.request.session.get('branch_actualy')
            branch_actualy = Branch.objects.get(id=branch_actualy)
            # Si el usuario es administrador y hay una sucursal seleccionada en la sesión,
            return Employee.objects.get_employees_branch(branch_actualy)
        
        # En otros casos, filtra por la sucursal del usuario
        return Employee.objects.get_employees_branch(branch)

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
        ]
        context['table_column'] = obtener_nombres_de_campos(User, *exclude_fields_user)
        # context['is_staff'] =self.request.user.is_staff iNNECESARIO, EN EL TEMPLATE YA EXISTE DEL PROPIO USUARIO
        return context
    

########################### DELETE ####################################

class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employes/employee_delete_page.html'
    success_url = reverse_lazy('employees_app:list_employee')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Realiza la eliminación suave
        return HttpResponseRedirect(self.get_success_url())

