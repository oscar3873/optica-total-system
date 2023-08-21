from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, UpdateView, View)

from .models import Employee
from .forms import EmployeeForm, EmployeeUpdateForm
from .services import data_pop
from applications.users.models import User

from applications.core.views import CustomUserPassesTestMixin
# Create your views here.
class EmployeeCreateView(LoginRequiredMixin, CustomUserPassesTestMixin, CreateView):
    template_name = 'employes/create_form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('core_app:home')


    def form_valid(self, form):
        user = User.objects.create_user(
            name=form.cleaned_data['name'],
            last_name=form.cleaned_data['last_name'],
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1'],
        )

        Employee.objects.create_user(
            user = user,
            **data_pop(form)
        )
        return HttpResponseRedirect(self.success_url)


class EmployeeUpdateView(LoginRequiredMixin, CustomUserPassesTestMixin, UpdateView):
    model = Employee
    template_name = 'employes/update_form.html'
    form_class = EmployeeUpdateForm
    success_url = reverse_lazy('core_app:home')


class EmployeeProfileView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 'employee' -> Empleado de la pk
        
        # Mas detalles para el perfil del empleado:
        # context['key'] = value

        return context