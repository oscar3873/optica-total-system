import os
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy

from django.views.generic import View
from django.views.generic import FormView, DetailView, UpdateView

from applications.core.models import Objetives
from django.utils import timezone


from project.settings.base import DATE_NOW
from .forms import UserCreateForm
from .models import User
from .forms import *
from .utils import *
from applications.branches.models import Branch, Branch_Objetives
from applications.employes.models import Employee_Objetives
from applications.core.mixins import CustomUserPassesTestMixin


# Create your views here.
class AdminProfileView(CustomUserPassesTestMixin, DetailView):
    model = User
    template_name = 'users/profile_admin.html'
    context_object_name = 'admin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_date = DATE_NOW.date()
        active_objetives = Objetives.objects.filter(start_date__lte=current_date,exp_date__gte=current_date)
        context['branch_objectives'] = Branch_Objetives.objects.filter(objetive__in=active_objetives)
        #context['branch_objectives'] = Branch_Objetives.active_objectives.all()
        context['employees_objectives'] = Employee_Objetives.objects.filter(objetive__in=active_objetives)
        return context


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
    

class AccountView(LoginRequiredMixin, UpdateView):
    template_name = 'users/user_account_page.html'
    model = User
    form_class = UserUpdateForm

    def get_context_data(self, **kwargs):
        user = self.get_object()
        branch_actualy = self.request.session.get('branch_actualy') or user.branch.pk
        branch_actualy = Branch.objects.get(pk=branch_actualy)

        context = super().get_context_data(**kwargs)
        context['form2'] = UpdatePasswordForm # Agregamos el segundo formulario al contexto
        context['change_image'] = ImagenChangeForm
        
        if not user.is_staff:
            context['objetives'] = user.employee_objetives.all()
        
        context['employee_objetives'], context['branch_objetives'] = get_emp_branch_objetives(branch_actualy, context['objetives']) 
        
        context['sales'] = user.sale_set.all()

        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Se actualizaron los datos con exito.")
        return reverse_lazy('users_app:account', kwargs={'pk': self.kwargs['pk']})
        

# View para validar formulario UpdatePasswordForm
class UpdatePasswordView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdatePasswordForm

    def form_valid(self, form):
        # Lógica para el formulario de UpdatePasswordForm (cambio de contraseña)
        # Cambia la contraseña del usuario y redirige al inicio de sesión
        if form.is_valid():
            self.object.set_password(form.cleaned_data['password'])
            self.object.save()
            messages.success(self.request, 'La contraseña se ha cambiado con exito.')
            return redirect('users_app:account', pk=self.kwargs['pk'])
        
        messages.error(self.request, 'La contraseña actual es incorrecta.')
        return redirect('users_app:account', pk=self.kwargs['pk'])
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error en el formulario de cambio de contraseña.')
        return redirect('users_app:account', pk=self.kwargs['pk'])


class UserChangeImagen(FormView):
    template_name = 'users/user_account_page.html'
    form_class = ImagenChangeForm

    def form_valid(self, form):
        from PIL import Image
        from project.settings.local import MEDIA_ROOT

        pk = self.kwargs['pk']
        user_profile = User.objects.get(pk=pk)
        new_image = form.cleaned_data['imagen']

        if new_image:
            image = Image.open(new_image)
            image = fix_image_orientation(image)  # Corregir la orientación si es necesario
            image.thumbnail((500, 500)) # Re-dimensionar imagen

            if user_profile.imagen:
                user_profile.imagen.delete()
                os.remove(user_profile.imagen.path)

            # Guardar la imagen en la carpeta profile en la misma ubicación
            name_img = user_profile.first_name[0] + user_profile.last_name[0] + str(user_profile.pk)
            image_path = os.path.join(MEDIA_ROOT, "profile", f'{name_img}.jpg')
            image.save(image_path, format='JPEG')

            user_profile.imagen = os.path.join("profile", f'{name_img}.jpg')
            user_profile.save()

            messages.success(self.request, 'Imagen de perfil actualizada correctamente')
        else:
            messages.error(self.request, 'Debes seleccionar una imagen válida')
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['pk']
        user_profile = User.objects.get(pk=pk)
        # Especifica la URL a la que deseas redirigir después de guardar la imagen
        return reverse_lazy('users_app:account', kwargs={'pk': user_profile.pk})