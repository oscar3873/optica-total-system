from typing import Any, Optional
from django.db import models
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, UpdateView, FormView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from .models import Employee
from .forms import EmployeeForm
from applications.users.models import User

from applications.core.mixins import CustomUserPassesTestMixin
# Create your views here.
class EmployeeCreateView(CustomUserPassesTestMixin, FormView):
    template_name = 'employes/employee_form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        user_data = {
            'first_name': form.cleaned_data['first_name'],
            'last_name': form.cleaned_data['last_name'],
            'username': form.cleaned_data['username'],
            'email': form.cleaned_data['email'],
            'password': form.cleaned_data['password1'],
            'branch': form.cleaned_data['branch'],
        }
        user = User.objects.create_user(**user_data)
        
        employee_data = {
            'user': user,
            'user_made': self.request.user,
            'first_name': form.cleaned_data['first_name'],
            'last_name': form.cleaned_data['last_name'],
            'phone_number': form.cleaned_data['phone_number'],
            'dni': form.cleaned_data['dni'],
            'birth_date': form.cleaned_data['birth_date'],
            'address': form.cleaned_data['address'],
        }
        Employee.objects.create(**employee_data)
        
        return super().form_valid(form)



class EmployeeUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Employee
    template_name = 'employes/employee_form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.instance.user_made = self.request.user
        return super().form_valid(form)




############## UNICA VIEW DISPONIBLE PARA EL USO #############
class EmployeeProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'employee'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')  # Obtén el valor del parámetro 'pk' de la URL
        try:
            employee = User.objects.get(pk=pk)
        except:
            employee = None
        return employee

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # object = 'EMPLEADO'
        
        # Mas detalles para el perfil del empleado:
        # context['key'] = value

        return context