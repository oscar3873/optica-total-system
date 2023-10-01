from typing import Any
from django import forms
from .models import User
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator

from applications.core.mixins import ValidationFormMixin
from applications.core.forms import PersonForm
# from applications.branches.models import Branch

class UserCreateForm(PersonForm):
    """
    Formulario para crear un usuario nuevo.
        fields: [first_name, last_name, email, password(1,2), dni, phone_number, ]
    """
    username = forms.CharField(
        required = False,
        widget = forms.TextInput(attrs={
            'placeholder' : 'usuario',
            'class' : 'form-control',
            'autocomplete' : 'off',
        }),
        validators=[RegexValidator(r'^[a-zA-Z0-9_]+$', 'El nombre de usuario solo puede contener letras, números y guiones bajos.')]
    )
    
    password = forms.CharField(
        required = False, 
        widget = forms.PasswordInput(attrs={
            'placeholder' : 'Contraseña',
            'autocomplete' : "off",
            'class' : 'form-control'
        }),
        validators=[RegexValidator(r'^[a-zA-Z0-9_]+$', 'El nombre de usuario solo puede contener letras, números y guiones bajos.')]
    )
    
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder' : 'Repetir contraseña',
            'autocomplete' : "off",
            'class' : 'form-control'
            })
    )

    imagen = forms.ImageField(
        required=False,  # Hacer que la carga de la imagen sea opcional
        widget=forms.FileInput(attrs={
            'class': 'form-control'
            }),
    )

    class Meta:
        model = User
        fields = ['email', 'username','first_name', 'last_name', 'birth_date', 'dni', 'phone_number','phone_code', 'address']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username: 
            first_name = str(self.cleaned_data.get('first_name'))
            last_name = str(self.cleaned_data.get('last_name'))
            username = (first_name + last_name).lower()
        self.validate_username(username)
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            password = 'opticatotal'
        self.validate_length(password, 6, 'La contraseña debe tener al menos 6 carácteres')
        return password
    
    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        if not password2:
            password2 = 'opticatotal'
        self.validate_length(password2, 6, 'La contraseña debe tener al menos 6 carácteres')
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            email = self.clean_username() + '@opticatotal.com'
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("El correo ingresado ya está en uso.")
        except User.DoesNotExist:
            return email

    def clean(self):
        cleaned_data = super().clean()
        if not "username" in cleaned_data:
            cleaned_data['username'] = self.clean_username()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password and password2 and password != password2:
            self.add_error('password2', 'Las contraseñas no coinciden')
        return cleaned_data
    
    
class UserUpdateForm(PersonForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
    
    class Meta:
        model = User
        fields = ('email','first_name', 'last_name','dni', 'phone_code','phone_number', 'address', 'birth_date')

class LoginForm(forms.Form):
    """Formulario para iniciar sesión."""
    
    username = forms.CharField(
        label='Usuario',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese su nombre de usuario',
            'class' : 'form-control',
            'autocomplete' : 'off',
            }),
    )
    
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ingrese su contraseña',
            'class' : 'form-control'
            })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('El usuario o contraseña son incorrectos.')
        return cleaned_data
    

class UpdatePasswordForm(ValidationFormMixin):
    
    passwordCurrent = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña actual',
            'class' : 'form-control',
            'id': 'id_passwordCurrent', # Para que lo identifique con ajax
            })
    )

    password = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Nueva contraseña',
            'class' : 'form-control'
            })
    )
    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita nueva contraseña',
            'class' : 'form-control'
            })
    )

    def clean_passwordCurrent(self):
        passwordCurrent = self.cleaned_data.get('passwordCurrent')
        user = self.instance  # Obtiene la instancia de usuario actual

        if user and not authenticate(username=user.username, password=passwordCurrent):
            raise forms.ValidationError('La contraseña actual es incorrecta')
        return passwordCurrent
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        password = password
        self.validate_length(password, 6, 'La contraseña debe tener al menos 6 carácteres')
        return password
    
    def clean_password2(self):
        password = self.cleaned_data.get('password2')
        password = password
        self.validate_length(password, 6, 'La contraseña debe tener al menos 6 carácteres')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password and password2 and password != password2:
            self.add_error('password2', 'Las contraseñas no coinciden')
        return cleaned_data
    
    class Meta:
        model=User
        fields = ("passwordCurrent","password","password2")


class ImagenChangeForm(forms.ModelForm):
    imagen = forms.ImageField(
        required=False,  # Hacer que la carga de la imagen sea opcional
        widget=forms.FileInput(attrs={
            'class': 'form-control-file'
            }),
    )
    class Meta:
        model = User
        fields = ['imagen',]
