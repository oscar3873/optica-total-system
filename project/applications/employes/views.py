from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, UpdateView, View)

from .models import Employee
from .forms import EmployeeForm, EmployeeUpdateForm
from .services import data_pop
from applications.users.models import User


# Create your views here.
class EmployeeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
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
        if not self.request.user.is_authenticated:
            return super(LoginRequiredMixin, self).handle_no_permission()
        else:
            context = {}
            return render(self.request, 'users/denied_permission.html', context)


class EmployeeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    template_name = 'employes/update_form.html'
    form_class = EmployeeUpdateForm
    success_url = reverse_lazy('core_app:home')

    def test_func(self):
        # Define aquí tu lógica de prueba personalizada para la actualización
        return self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super(LoginRequiredMixin, self).handle_no_permission()
        else:
            context = {}
            return render(self.request, 'users/denied_permission.html', context)


class EmployeeProfileView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 'employee' -> Empleado de la pk
        
        # Mas detalles para el perfil del empleado:
        # context['key'] = value

        return context