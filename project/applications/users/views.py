from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views.generic import View
from django.views.generic import FormView, DetailView, UpdateView


from .forms import UserCreateForm
from .models import User
from .forms import *
from .utils import generate_profile_img_and_assign
from applications.branches.models import Branch
from applications.core.mixins import CustomUserPassesTestMixin


# Create your views here.
class AdminProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile_admin.html'
    context_object_name = 'admin'

    def get_object(self, queryset=None):
        pk = self.request.user.pk  # Obtén la pk del usuario
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
        """  # Extraer los valores del código telefónico y el número de teléfono
        phone_code = form.cleaned_data.pop('phone_code', None)
        phone_number = form.cleaned_data.pop('phone_number', None)

        # Combinar el código telefónico y el número de teléfono si ambos existen
        if phone_code and phone_number:
            full_phone_number = f"{phone_code}{phone_number}"
            form.cleaned_data['phone_number'] = full_phone_number """

        form.cleaned_data.pop('password2')
        form.cleaned_data.pop('phone_code')
        branch_actualy = self.request.session.get('branch_actualy')
        branch_actualy = Branch.objects.get(id=branch_actualy)
        user = User.objects.create_admin(**form.cleaned_data, branch=branch_actualy) # Funcion que crea ADMINIS

        if not form.cleaned_data.get('imagen'):
            generate_profile_img_and_assign(user)

        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        self.request.session['branch_actualy'] = int(self.request.user.branch.id)
        
        if next_url:
            return redirect(next_url)  # Redirige a la URL especificada en 'next'
        
        return redirect(self.success_url)  # Si no hay 'next', redirige a una URL predeterminada
    

class LogoutView( View):
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
    
    
class AccountView(UpdateView):
    template_name = 'users/user_account_page.html'
    model = User
    form_class = UserUpdateForm
    form2_class = UpdatePasswordForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form2'] = self.get_form(self.form2_class)  # Se agrega el segundo formulario al contexto
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form2 = self.get_form(self.form2_class)

        if 'form2' in request.POST:
            # Si se envió el formulario de cambio de contraseña
            if form2.is_valid():
                # Procesa el formulario de cambio de contraseña
                self.object.set_password(form2.cleaned_data['password'])
                self.object.save()
                return redirect("users_app:login")
            else:
                # El formulario de cambio de contraseña no es válido
                context = self.get_context_data(form2=form2)
                return self.render_to_response(context)
        else:
            # Si no se envió el formulario de cambio de contraseña,
            # procesa el formulario de actualización de datos de usuario
            return super().post(request, *args, **kwargs)