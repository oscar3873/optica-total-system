from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, UpdateView, FormView,ListView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import get_object_or_404

from .forms import EmployeeCreateForm,EmployeeUpdateForm
from applications.core.mixins import CustomUserPassesTestMixin
from applications.branches.models import Branch
from applications.users.models import User, Employee
from applications.users.forms import UserUpdateForm

#from .core.utils import obtener_nombres_de_campos
from .utils import obtener_nombres_de_campos
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

class EmployeeUpdateView(UpdateView):
    model = Employee
    template_name = 'users/employee_update_page.html'
    form_class = EmployeeUpdateForm
    def form_valid(self, form):
        user_form = UserUpdateForm(self.request.POST, instance=self.object.user)
        if user_form.is_valid():
            user = user_form.save()
            form.save()
            return redirect('employees_app:list_employee')
        else:
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

    def get_form_kwargs(self):
        # Obtener la instancia de Employee que se va a editar
        employee_instance = get_object_or_404(Employee, pk=self.kwargs['pk'])
        
        # Pasar la instancia al formulario como kwarg
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = employee_instance
        return kwargs


# Probando cuenta, no me deja hacer un update de los datod de empleado

class AccountView(UpdateView):
    template_name = 'users/employee_account_page.html'
    form_class = UserUpdateForm
    model = User
    success_url = reverse_lazy('employees_app:list_employee')
    """
    def get_object(self,queryset=None):
        pk = self.kwargs.get('pk')
        print("###############\n\n\n\n\n")
        print(pk)
    
    def form_valid(self, form):
        self.user.first_name = form.cleaned_data['first_name']
    
        if form.is_valid():
            form.save()
            return redirect('employees_app:list_employee')
        else:
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

    
    def get_object(self, queryset=None):
        #Obtén el valor del parámetro 'pk' de la URL, este 
        #parametro, puede ser la pk de un user, comprobar que esta pk esta relacionada 
        #con alguna pk de la tabla users_employee
        pk = self.request.user.pk
        try:
            #Me aseguro de que el usuario que esta realizando la accion sea un empleado
            if not self.request.user.is_staff:
                employee = Employee.objects.get(user_id=pk)
            else:
                employee = None
            #busco en la tabla user de la base de datos un usuario con user_id=pk
        except Employee.DoesNotExist:
            #si no encuentro lo pongo en None para manejar las vistas en los templates
            employee = None
        return employee
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.request.user.pk
        context["pk"] = pk
        return context
    
    def get_form_kwargs(self): 
        # Obtener la instancia de Employee que se va a editar
        employee_instance = get_object_or_404(Employee, pk=self.kwargs['pk'])
        
        # Pasar la instancia al formulario como kwarg
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = employee_instance
        return kwargs """


""" print("#############################\n\n\n\n\n\n")
print(f"user_form = {user_form}")
print("#############################\n\n\n\n\n\n")
"""        

############## UNICA VIEW DISPONIBLE PARA EL USO #############
# Perfil de empleado
class EmployeeProfileView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'users/profile.html'
    context_object_name = 'employee'

    def get_object(self, queryset=None): 
        """ Obtén el valor del parámetro 'pk' de la URL, este 
        parametro, puede ser la pk de un user, comprobar que esta pk esta relacionada 
        con alguna pk de la tabla users_employee"""
        pk = self.request.user.pk
        try:
            if not self.request.user.is_staff:
                employee = Employee.objects.get(user_id=pk)
            else:
                employee = None
            #busco en la tabla user de la base de datos un usuario con user_id=pk
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
        branch = self.request.user.branch
        branch_actualy = self.request.session.get('branch_actualy')

        if  self.request.user.is_staff and branch_actualy:
            branch_actualy = Branch.objects.get(id=branch_actualy)
            # Si el usuario es administrador y hay una sucursal seleccionada en la sesión,
            return Employee.objects.filter(branch=branch_actualy, deleted_at=None)
        
        # En otros casos, filtra por la sucursal del usuario
        return Employee.objects.filter(branch=branch, deleted_at=None)

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

