from django import forms
from .models import User, Employee
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator

from applications.core.mixins import ValidationFormMixin
from applications.core.forms import PersonForm
from applications.branches.models import Branch

class UserCreateForm(PersonForm):
    """
    Formulario para crear un usuario nuevo.
        fields: [first_name, last_name, email, password(1,2), dni, phone_number, ]
    """
    
    first_name = forms.CharField(
        required = True,
        widget = forms.TextInput(attrs={
            'placeholder' : 'Ej: Javier',
            'class' : 'form-control',
            'autocomplete' : 'off',
        }),
        validators=[RegexValidator(r'^[a-zA-Z]+$', 'El nombre solo puede contener letras.')]
    )
    
    last_name = forms.CharField(
        required = True,
        widget = forms.TextInput(attrs={
            'placeholder' : 'Ej: Torres',
            'class' : 'form-control',
            'autocomplete' : 'off',
        }),
        validators=[RegexValidator(r'^[a-zA-Z]+$', 'El apellido solo puede contener letras.')]
    )


    dni = forms.CharField(
        required = True,
        widget = forms.TextInput(attrs={
            'placeholder' : 'Ej: 32432567',
            'class' : 'form-control',
            'autocomplete' : 'off',
        }),
        validators=[RegexValidator(r'^[a-zA-Z0-9]+$', 'Ingrese un DNI válido.')]
    )


    address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder' : 'Ej: Zuviria 580',
            'class' : 'form-control',
            'autocomplete' : 'off',
            })
    )


    phone_number = forms.IntegerField(
        required = True,
        widget = forms.TextInput(attrs={
            'placeholder' : 'Ej: 3875123321',
            'class' : 'form-control',
            'autocomplete' : 'off',
        }),
    )

    birth_date = forms.DateField(
        required = True,
        widget = forms.DateInput(attrs={
            'placeholder' : 'Fecha de Nacimiento',
            'class' : 'form-control',
            'type' : 'date',
            'autocomplete' : 'off',
        }),
    )

    username = forms.CharField(
        required = True,
        widget = forms.TextInput(attrs={
            'placeholder' : 'Ej: Javi28',
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

    email = forms.EmailField(
        required = False,
        widget = forms.EmailInput(attrs={
            'placeholder' : 'Ej: javier_torres28@gmail.com',
            'class' : 'form-control',
            'autocomplete' : 'off',
        })
    )

    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        label='Sucursal',
        empty_label='Elija una sucursal',
        required=True,
        widget=forms.Select(attrs={
            'placeholder' : 'Sucursal',
            'class' : 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name', 'birth_date', 'dni', 'phone_number', 'address', 'branch')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        username = username.lower()
        self.validate_username(username)
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        password = password.lower()
        self.validate_length(password, 6, 'La contraseña debe tener al menos 6 carácteres')
        return password
    
    def clean_password2(self):
        password2 = self.cleaned_data.get('password')
        password2 = password2.lower()
        return password2

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password and password2 and password != password2:
            self.add_error('password2', 'Las contraseñas no coinciden')
        return cleaned_data
    
    
class LoginForm(forms.Form):
    """Formulario para iniciar sesión."""
    
    username = forms.CharField(
        label='Usuario',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese su nombre de usuario',
            }),
    )
    
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña',
                                          'class' : 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Correo electrónico o contraseña incorrectos')
        return cleaned_data
    

class UpdatePasswordForm(ValidationFormMixin):

    passwordCurrent = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña actual',
            'class' : 'form-control'
            })
    )

    password = forms.CharField(
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

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username = username.lower()
        self.validate_username(username)
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        password = password.lower()
        self.validate_length(password, 6, 'La contraseña debe tener al menos 6 carácteres')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password and password2 and password != password2:
            self.add_error('password2', 'Las contraseñas no coinciden')
        return cleaned_data
    

class EmployeeCreateForm(UserCreateForm):
    employment_date = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
            })
    )
    class Meta:
        model = Employee
        fields = ['employment_date',]

    def clean_employment_date(self):
        employment_date = self.cleaned_data['employment_date']
        self.validate_date(employment_date)
        return employment_date