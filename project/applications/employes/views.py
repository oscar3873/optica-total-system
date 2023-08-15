from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Employee
from .forms import EmployeeCreateForm
from applications.core.forms import PersonForm
from applications.core.models import Person

from django.views.generic import (CreateView, DetailView, UpdateView, View)

# Create your views here.
class EmployeeCreateView(UserPassesTestMixin, CreateView):
    model = Employee
    template_name = 'employes/employee_create_form.html'
    form_class = EmployeeCreateForm
    success_url = reverse_lazy('core_app:home')

    def test_func(self):
        return self.request.user.is_staff and self.request.user.is_superuser

    def form_valid(self, form):
        employee = form.save(commit=False)
        form.cleaned_data.pop('from_branch')
        person_form = Person.objects.create_person_dict(**form.cleaned_data)

        employee.person = person_form
        employee.save()
        
        return super().form_valid(form)


class EmployeeProfileView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 'employee' -> Empleado de la pk
        
        # Mas detalles para el perfil del empleado:
        # context['key'] = value

        return context
    

class EmployeeUpdate_Person(UserPassesTestMixin, UpdateView):
    model = Person
    template_name = 'employes/employee_update_form.html'
    form_class = PersonForm