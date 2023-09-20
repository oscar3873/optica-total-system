from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views.generic import View
from django.views.generic.edit import (FormView,)
from django.views.generic import (DetailView,UpdateView)

from .forms import UserCreateForm, LoginForm, UpdatePasswordForm,UserUpdateForm
from .models import User
from applications.core.mixins import CustomUserPassesTestMixin


# Create your views here.
class AdminProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile_admin.html'
    context_object_name = 'admin'

    def get_object(self, queryset=None):
        # pk = self.request.user.pk  # Obtén la pk del usuario
        pk = self.kwargs.get('pk') # PK traido de la URL
        try:
            admin = User.objects.get(pk=pk)
            #busco en la tabla user de la base de datos un usuario con pk=pk,is_staff=False,is_superuser=False,role='EMPLEADO'
        except User.DoesNotExist:
            #si no encuentro lo pongo en None para manejar las vistas en los templates
            admin = None
        return admin


class AdminCreateView(CustomUserPassesTestMixin, FormView): # CREACION DE ADMINIS
    template_name = "users/signup.html"
    form_class = UserCreateForm
    success_url = reverse_lazy('core_app:home')
    
    def form_valid(self, form):
        # Extraer los valores del código telefónico y el número de teléfono
        phone_code = form.cleaned_data.pop('phone_code', None)
        phone_number = form.cleaned_data.pop('phone_number', None)

        # Combinar el código telefónico y el número de teléfono si ambos existen
        if phone_code and phone_number:
            full_phone_number = f"{phone_code}{phone_number}"
            form.cleaned_data['phone_number'] = full_phone_number

        form.cleaned_data.pop('password2')
        form.cleaned_data.pop('phone_code')
        User.objects.create_admin(**form.cleaned_data) # Funcion que crea ADMINIS
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Le paso este contexto al template, para no poner el input
        # de fecha de alta de empleado cuando se este creando un 
        # administrador
        context["admin"] = True 
        return context
    


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