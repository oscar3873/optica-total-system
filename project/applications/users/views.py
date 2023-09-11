from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views.generic import View
from django.views.generic.edit import (FormView,)

from .forms import UserCreateForm, LoginForm, UpdatePasswordForm, EmployeeCreateForm
from .models import User, Employee
from applications.core.mixins import CustomUserPassesTestMixin


# Create your views here.
class EmployeeCreateView(CustomUserPassesTestMixin, FormView): # CREACION DE EMPLEADOS
    template_name = "users/signup.html"
    form_class = EmployeeCreateForm
    success_url = reverse_lazy('core_app:home')
    
    def form_valid(self, form):
        form.cleaned_data.pop('password2')
        Employee.objects.create(
            user_made = self.request.user,
            employment_date = form.cleaned_data.pop('employment_date'),
            user = User.objects.create_user(**form.cleaned_data) # Funcion que crea EMPLEADOS
            )
        return super().form_valid(form)
    

class AdminCreateView(CustomUserPassesTestMixin, FormView): # CREACION DE ADMINIS
    template_name = "users/signup.html"
    form_class = UserCreateForm
    success_url = reverse_lazy('core_app:home')
    
    def form_valid(self, form):
        form.cleaned_data.pop('password2')
        User.objects.create_admin(**form.cleaned_data) # Funcion que crea ADMINIS
        return super().form_valid(form)

 
class LoginView(views.RedirectURLMixin, FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('core_app:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        
        next_url = self.request.GET.get('next')  # Obtiene el valor del par�metro 'next' de la URL
        
        if next_url:
            return redirect(next_url)  # Redirige a la URL especificada en 'next'
        
        return redirect(self.success_url)  # Si no hay 'next', redirige a una URL predeterminada
    

class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, template_name='users/logout.html', context={})
    

class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = "users/update_password.html"
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:login')
    login_url = reverse_lazy('users_app:login')
    
    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username=usuario.email,
            password=form.cleaned_data['passwordCurrent']
        )
        
        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()
        
        logout(self.request)
        return super().form_valid(form)