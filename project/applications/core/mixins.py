from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from datetime import timedelta
from django import forms

from applications.users.models import User
from project.settings.base import DATE_NOW

class ValidationFormMixin(forms.ModelForm):
    def validate_length(self, field_value, min_length, error_message):
        """
        Valida longitud de una cadena.
            Para nombres, apellidos, direcciones, telefonos, etc.
            Muestra el error mandado por argumento.
        """
        if field_value is not None:
            field_value = str(field_value)
            if len(field_value) < min_length:
                raise forms.ValidationError(error_message)

    def validate_birth_date(self, birth_date):
        """
        Valida fecha de nacimiento.
            Debe tener por lo menos 3 meses de vida o no superar los 85 años.
        """
        if birth_date :
            if birth_date >= DATE_NOW.date() - timedelta(days=30):
                raise forms.ValidationError('La fecha establecida no puede registrarse.')
            age_limit = DATE_NOW.date() - timedelta(days=85*365)
            if birth_date <= age_limit:
                raise forms.ValidationError('La fecha establecida no puede superar los 85 años.')

    def validate_email(self, email):
        """
        Valida la duplicacion de email en el sistema
        """
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya existe')

    def validate_username(self, username):
        """
        Valida la duplicacion de username
        """
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El usuario ya existe')
        
    def validate_date(self, date):
        """
        Valida que la fecha ingresada no sea al futuro
        """
        if date:
            if date > DATE_NOW.date():
                raise forms.ValidationError('La fecha establecida no puede registrarse.')
        else:
            raise forms.ValidationError('Este campo es nesesario.')

class CustomUserPassesTestMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Clase mixin para requerir autenticacion del usuario administrador
    """
    def test_func(self):
        """
        Para la verificacion de Administrador
        """
        return self.request.user.is_staff

    def handle_no_permission(self):
        """
        Renderiza un template con el acceso denegado a quien quiera acceder a una pestaña sin permiso
        """
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        else:
            context = {}
            return render(self.request, 'users/denied_permission.html', context)
