from django import forms
from django.core.validators import RegexValidator

from .models import Person
from .mixins import ValidationFormMixin

class PersonForm(ValidationFormMixin):
    first_name = forms.CharField(
        required = True,
        widget = forms.TextInput(attrs={
            'placeholder' : 'Nombre',
            'class' : 'form-control',
            'autofocus' : '',
            'type' : 'text',
            'pattern': '^[a-zA-Z\s]+$'
        }),
        validators=[RegexValidator(r'^[a-zA-Z\s]+$', 'El nombre solo puede contener letras y espacios.')]

    )
    
    last_name = forms.CharField(
        required = True,
        widget = forms.TextInput(attrs={
            'placeholder' : 'Apellido',
            'class' : 'form-control',
            'type' : 'text',
            'pattern': '^[a-zA-Z\s]+$'
        }),
        validators=[RegexValidator(r'[a-zA-Z\s]+$', 'El apellido solo puede contener letras.')]
    )

    dni = forms.CharField(
        required = True,
        widget = forms.TextInput(attrs={
            'placeholder' : 'DNI',
            'class' : 'form-control',
            'type' : 'text',
            'pattern' : '[0-9]+'
        }),
        validators=[RegexValidator(r'^[0-9]+$', 'Ingrese un DNI válido.')]
    )

    address = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder' : 'Domicilio',
            'class' : 'form-control',
            'type' : 'text',
            'pattern': '^[a-zA-Z0-9]+([a-zA-Z0-9 ]*[a-zA-Z0-9]+)*$'

            })
    )

    phone_number = forms.IntegerField(
        required = True,
        widget = forms.TextInput(attrs={
            'placeholder' : 'Telefono de contacto',
            'class' : 'form-control',
            'type' : 'numeric',
            'pattern' : '[0-9]+'
        }),
    )

    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'placeholder': 'Fecha de Nacimiento',
                'type': 'date',
                'class': 'form-control'
            },
            format='%Y-%m-%d',
        )
    )

    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder' : 'Correo electrónico',
            'class': 'form-control',
            'type' : 'email',
            'pattern' : '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            }
        )
    )

    class Meta:
        model = Person
        fields = '__all__'

    def clean_first_name(self):
        name = self.cleaned_data['first_name']
        self.validate_length(name, 3, "Ingrese un nombre válido.")
        return name.capitalize()
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        self.validate_length(last_name, 3, "Ingrese un apellido válido.")
        return last_name.capitalize()

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        self.validate_length(phone_number, 9, "Ingrese un número de teléfono válido")
        return phone_number

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        self.validate_length(dni, 7, "Ingrese un número de DNI válido.")
        return dni

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        self.validate_birth_date(birth_date)
        return birth_date
    
    def clean_address(self):
        address = self.cleaned_data['address']
        self.validate_length(address, 5, "Ingrese una dirección válida.")
        return address