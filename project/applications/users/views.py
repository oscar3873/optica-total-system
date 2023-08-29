from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views.generic import View
from django.views.generic.edit import (FormView,)

from .forms import UserCreateForm, LoginForm, UpdatePasswordForm
from .models import User



# Create your views here.
class UserCreateView(FormView): # PARA CREAR USUARIOS PUROS (RECOMENDADO PARA CREAR ADMINISTRADORES)
    template_name = "users/signup.html"
    form_class = UserCreateForm
    success_url = '/'
    
    def form_valid(self, form):
        data_user = {
            'first_name': form.cleaned_data['first_name'],
            'last_name': form.cleaned_data['last_name'],
            'username': form.cleaned_data['username'],
            'email': form.cleaned_data['email'],
            'password': form.cleaned_data['password1'],
            'branch': form.cleaned_data['branch'],
        }
        User.objects.create_user(**data_user) # Para empleados
        return super().form_valid(form)

 
class LoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('core_app:home')
    
    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        
        next_url = self.request.GET.get('next')  # Obtiene el valor del par�metro 'next' de la URL
        
        if next_url:
            return redirect(next_url)  # Redirige a la URL especificada en 'next'
        
        return redirect(self.success_url)  # Si no hay 'next', redirige a una URL predeterminada
    

class LogoutView(View):
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