from audioop import reverse
from typing import Any

from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DetailView, UpdateView, FormView, ListView, DeleteView
)
from django.db import models, transaction
from django.forms.models import BaseModelForm

from django.contrib.auth.mixins import LoginRequiredMixin

from applications.branches.models import Branch
from applications.core.mixins import CustomUserPassesTestMixin
from applications.users.models import User
from applications.users.forms import *
from applications.users.utils import generate_profile_img_and_assign

from .forms import EmployeeCreateForm, EmployeeUpdateForm
from .models import Employee
from .utils import obtener_nombres_de_campos

from django.contrib.auth import authenticate



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

        empleado = Employee.objects.create(
            user_made = user,
            employment_date = form.cleaned_data.pop('employment_date'),
            user = User.objects.create_user(**form.cleaned_data, branch=branch) # Funcion que crea EMPLEADOS
            )
    
        if not form.cleaned_data.get('imagen'):
            generate_profile_img_and_assign(empleado.user)
        
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

    # PARA CAMBIAR LA IMAGEN DEL USUARIO
    # def get_context_data(self, **kwargs):
    #         context = super().get_context_data(**kwargs)
    #         context["change_image"] = ImagenChangeForm(instance=self.get_object())
    #         return context


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
            "imagen",
        ]
        context['table_column'] = obtener_nombres_de_campos(User, *exclude_fields_user)
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

############################ Account ####################################
# En el template 'employes/employee_account_page.html'
# cada formulario tiene un action a UpdateUserInfoView y a UpdatePasswordView respectivamente 
class AccountView(LoginRequiredMixin, UpdateView):
    template_name = 'employes/employee_account_page.html'
    model = User
    form_class = UserUpdateForm
    form2_class = UpdatePasswordForm
    def get_context_data(self, **kwargs):
        is_editable = True
        context = super().get_context_data(**kwargs)
        context['form2'] = self.get_form(self.form2_class)  # Agregamos el segundo formulario al contexto
        return context

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


    def form_invalid(self, form):
        # Lógica para manejar errores en el formulario UserUpdateForm
        # Agregar mensajes de error al contexto
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def form2_invalid(self, form):
        # Lógica para manejar errores en el formulario UpdatePasswordForm
        # Agregar mensajes de error al contexto
        context = self.get_context_data(form2=form)
        return self.render_to_response(context)

#View para validar formulario UserUpdateForm
class UpdateUserInfoView(LoginRequiredMixin, UpdateView):
    template_name = 'employes/employee_account_page.html'
    model = User
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        employee = Employee.objects.get(pk=self.kwargs['pk'])
        return employee.user
    
    def get_success_url(self):
        return reverse_lazy('employees_app:account', kwargs={'pk': self.object.employee.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar el formulario UserUpdateForm al contexto
        password_update_form = UpdatePasswordForm(instance=self.object)  # Crea una instancia del formulario con el objeto actual
        context['form2'] = password_update_form
        return context

    def form_invalid(self, form):
        # Lógica para manejar errores en el formulario UserUpdateForm
        # Agregar mensajes de error
        context = self.get_context_data(form=form)
        messages.error(self.request, 'Error en el formulario de actualización de usuario.')
        return self.render_to_response(context)

# View para validar formulario UpdatePasswordForm
class UpdatePasswordView(LoginRequiredMixin, UpdateView):
    template_name = 'employes/employee_account_page.html'
    model = User
    form_class = UpdatePasswordForm

    def form_valid(self,form):
        # Lógica para el formulario de UpdatePasswordForm (cambio de contraseña)
        # Cambia la contraseña del usuario y redirige al inicio de sesión
        self.object.set_password(form.cleaned_data['password'])
        self.object.save()
        return redirect('users_app:logout')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar el formulario UserUpdateForm al contexto
        user_update_form = UserUpdateForm(instance=self.object)  # Crea una instancia del formulario con el objeto actual
        context['form'] = user_update_form
        return context

    def get_object(self, queryset=None):
        employee = Employee.objects.get(pk=self.kwargs['pk'])
        return employee.user

    
    def form_invalid(self, form):
        # Lógica para manejar errores en el formulario UpdatePasswordForm
        # Agregar mensajes de error al contexto
        context = self.get_context_data(form2=form)
        messages.error(self.request, 'Error en el formulario de cambio de contraseña.')
        return self.render_to_response(context)

# Funcion que se usa en la peticion ajax para validar la contraseña actual
def validate_password_current(request):
    if request.method == 'POST':
        password_current = request.POST.get('password_current')
        user = request.user  # Obtén al usuario actualmente autenticado
        if authenticate(username=user.username, password=password_current):
            return JsonResponse({'valid': True})
        else:
            return JsonResponse({'valid': False})
