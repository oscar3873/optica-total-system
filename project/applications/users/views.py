from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (CreateView, View)
from django.views.generic.edit import (FormView,)

from .forms import UserCreateForm, LoginForm, UpdatePasswordForm
from .models import User

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse


# Create your views here.
class UserCreateView(FormView):
    template_name = "users/signup.html"
    form_class = UserCreateForm
    success_url = '/'
    
    def form_valid(self, form):
        
        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
        
        )
        return super().form_valid(form)

 
class LoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = '/admin'
    
    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super().form_valid(form)
    

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
            password=form.cleaned_data['password1']
        )
        
        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()
        
        logout(self.request)
        
        return super().form_valid(form)