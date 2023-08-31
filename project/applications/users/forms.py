from django import forms
from .models import User
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator

from applications.core.mixins import ValidationFormMixin
from applications.branches.models import Branch

class UserCreateForm(ValidationFormMixin):
    """Formulario para crear un usuario nuevo."""
    
    first_name = forms.CharField(
        required = True,
        widget = forms.TextInput(attrs={
            'placeholder' : 'Nombre',
            'class' : 'form-control'
        }),
        validators=[RegexValidator(r'^[a-zA-Z0-9_]+$', 'El nombre solo puede contener letras, números y guiones bajos.')]
    )
    
    last_name = forms.CharField(
        required = True,
        widget = forms.TextInput(attrs={
            'placeholder' : 'Apellido',
            'class' : 'form-control'
        }),
        validators=[RegexValidator(r'^[a-zA-Z0-9_]+$', 'El apellido solo puede contener letras, números y guiones bajos.')]
    )

    username = forms.CharField(
        required = True,
        widget = forms.TextInput(attrs={
            'placeholder' : 'Usuario',
            'class' : 'form-control'
        }),
        validators=[RegexValidator(r'^[a-zA-Z0-9_]+$', 'El nombre de usuario solo puede contener letras, números y guiones bajos.')]
    )
    
    password1 = forms.CharField(
        required = True, 
        widget = forms.PasswordInput(attrs={
            'placeholder' : 'Contraseña',
            'autocomplete' : "off",
            'class' : 'form-control'
        })
    )
    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder' : 'Repetir contraseña',
            'autocomplete' : "off",
            'class' : 'form-control'
            })
    )

    email = forms.EmailField(
        required = False,
        widget = forms.EmailInput(attrs={
            'placeholder' : 'Correo',
            'class' : 'form-control'
        })
    )

    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        label='Sucursal',
        required=True,
    )

    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name', 'branch', 'birth_date', 'dni', 'phone_number')
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        self.validate_length(first_name, 3, 'El nombre debe tener al menos 3 caracteres')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        self.validate_length(last_name, 3, 'El apellido debe tener al menos 3 caracteres')
        return last_name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        self.validate_email(email)
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        self.validate_username(username)
        return username
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        self.validate_length(password1, 6, 'La contraseña debe tener al menos 6 carácteres')
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden')
        return cleaned_data
    
    
class LoginForm(forms.Form):
    """Formulario para iniciar sesión."""
    
    email = forms.EmailField(
        label='Correo electrónico',
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Ingrese su correo',
                                       })
    )
    
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Correo electrónico o contraseña incorrectos')
        return cleaned_data
    

class UpdatePasswordForm(forms.Form):

    passwordCurrent = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña actual',
            'class' : 'form-control'
            })
    )

    password1 = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Nueva contraseña'
            })
    )
    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita nueva contraseña'
            })
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden')
        return cleaned_data