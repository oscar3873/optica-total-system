from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, UpdateView, FormView)

from .models import Employee
from .forms import EmployeeForm
from applications.users.models import User

from applications.core.views import CustomUserPassesTestMixin
# Create your views here.
class EmployeeCreateView(LoginRequiredMixin, CustomUserPassesTestMixin, FormView):
    model = Employee
    template_name = 'employes/employee_form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.cleaned_data.pop('password2')
        user = User.objects.create_user(
            name=form.cleaned_data['name'],
            last_name=form.cleaned_data['last_name'],
            username=form.cleaned_data.pop('username'),
            email=form.cleaned_data.pop('email'),
            password=form.cleaned_data.pop('password1'),
        )
        employee_data = form.cleaned_data.copy()
        employee_data['user'] = user
        employee_data['user_made'] = self.request.user
        Employee.objects.create(**employee_data)
        return super().form_valid(form)



class EmployeeUpdateView(LoginRequiredMixin, CustomUserPassesTestMixin, UpdateView):
    model = Employee
    template_name = 'employes/employee_form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('core_app:home')


class EmployeeProfileView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 'employee' -> Empleado de la pk
        
        # Mas detalles para el perfil del empleado:
        # context['key'] = value

        return context