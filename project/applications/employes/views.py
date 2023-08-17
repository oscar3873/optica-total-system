from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Employee
from .forms import EmployeeForm
from .services import data_pop
from applications.users.models import User

from django.views.generic import (CreateView, DetailView, UpdateView, View)

# Create your views here.
class EmployeeCreateView(UserPassesTestMixin, CreateView):
    model = Employee
    template_name = 'employes/create_form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('core_app:home')

    def test_func(self):
        """
        Para la verificacion de Administrador
        """
        return self.request.user.is_staff

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1']
        )

        Employee.objects.create_user(
            user = user,
            **data_pop(form)
        )
        return HttpResponseRedirect(self.success_url)
    
    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        else:
            context = {}  # Puedes agregar datos al contexto si es necesario
            return render(self.request, 'users/denied_permission.html', context)


    def get_permission_denied_message(self):
        return {"No tienes permiso para acceder a esta página."}



class EmployeeProfileView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 'employee' -> Empleado de la pk
        
        # Mas detalles para el perfil del empleado:
        # context['key'] = value

        return context