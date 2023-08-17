from django import forms
from .models import User
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator



class UserCreateForm(forms.ModelForm):
    """Formulario para crear un usuario nuevo."""
    
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
    

    class Meta:
        model = User
        fields = ('email', 'username',)
    
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya existe')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El usuario ya existe')
        return username
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 and len(password1) < 6:
            raise forms.ValidationError('La contraseña debe tener al menos 6 caracteres')
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