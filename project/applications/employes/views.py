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

# Para la generacion de excel
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.dimensions import ColumnDimension

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

        Employee.objects.create(
            user_made = user,
            employment_date = form.cleaned_data.pop('employment_date'),
            user = User.objects.create_user(**form.cleaned_data, branch=branch) # Funcion que crea EMPLEADOS
            )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al cargar los datos. Por favor, revise los campos.')
        return super().form_invalid(form)


class EmployeeUpdateView(UpdateView):
    model = Employee
    template_name = 'employes/components/employee_update_form.html'
    form_class = EmployeeUpdateForm
    success_url = reverse_lazy('employees_app:list_employee')
    
    def form_valid(self, form):
        employee = form.instance

        if form.is_valid():
            employee.user.first_name = form.cleaned_data.get('first_name')
            employee.user.last_name = form.cleaned_data.get('last_name')
            employee.user.dni = form.cleaned_data.get('id')
            employee.user.address = form.cleaned_data.get('address')
            employee.user.phone_number = form.cleaned_data.get('phone_number')
            employee.user.phone_code = form.cleaned_data.get('phone_code')
            employee.user.birth_date = form.cleaned_data.get('birth_date')

            employee.user.save()

            messages.success(self.request, 'Se actualizo los datos de %s, %s con exito.''.' % (employee.user.last_name, employee.user.first_name))
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
    

################################## LISTING  ##################################
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
    
    def form_valid(self,form):
        employee = self.get_object()
        user = employee.user
        user.is_active = False  # Realiza la eliminación suave del usuario y por consecuencia, el empleado
        user.delete()
        employee.delete()
        return HttpResponseRedirect(self.get_success_url())

########################### GENERACION EXCEL ####################################

def export_employee_list_to_excel(request):
    branch = request.user.branch

    branch_actualy = request.session.get('branch_actualy')
    if request.user.is_staff and branch_actualy:
        branch = Branch.objects.get(id=branch_actualy)
    
    queryset = Employee.objects.get_employees_branch(branch).filter(deleted_at=None)
    
    workbook = Workbook()
    worksheet = workbook.active

    # Estilos personalizados
    header_style = {
        "font": Font(name='Arial', size=14, bold=True, color='d8e2ef'),
        "fill": PatternFill(start_color='0b1727', end_color='0b1727', fill_type='solid')
    }

    # Define los encabezados de las columnas
    exclude_fields_user = ["deleted_at", "created_at", "updated_at"]
    headers = [ campo[1]  for campo in obtener_nombres_de_campos(Employee, *exclude_fields_user)]

    # Aplicar estilos a los encabezados y escribir los encabezados
    for col_num, header in enumerate(headers, 1):
        cell = worksheet.cell(row=1, column=col_num, value=header)
        cell.font = header_style["font"]
        cell.fill = header_style["fill"]

    # Modificar el ancho de la columna (ajustar según tus necesidades)
    worksheet.column_dimensions[worksheet.cell(row=1, column=2).column].width = 20
    worksheet.column_dimensions[worksheet.cell(row=1, column=3).column].width = 20
    worksheet.column_dimensions[worksheet.cell(row=1, column=4).column].width = 30

    # Agregar los datos de los empleados a la hoja de cálculo
    for row_num, employee in enumerate(queryset, 2):
        worksheet.cell(row=row_num, column=1, value=str(employee.id))
        worksheet.cell(row=row_num, column=2, value=str(employee.user_made))
        worksheet.cell(row=row_num, column=3, value=employee.user.get_full_name())
        worksheet.cell(row=row_num, column=4, value=employee.employment_date)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=employee_data.xlsx'

    workbook.save(response)

    return response