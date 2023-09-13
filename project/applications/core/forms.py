from django import forms
from django.core.validators import RegexValidator,EmailValidator

from .models import Person, Objetives
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

        # Expresión regular para validar números de teléfono de varios países.
        phone_number_pattern = re.compile(r'^(?:\+?[0-9]{1,3})?[0-9]{6,}$')

        if not phone_number_pattern.match(str(phone_number)):
            raise forms.ValidationError("Ingrese un número de teléfono válido.")

        return phone_number

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        self.validate_length(phone_number, 9, "Ingrese un número de teléfono válido")
        return phone_number
    
    def clean_dni(self):
        dni = self.cleaned_data['dni']

        # Expresión regular para validar DNI: 7 dígitos seguidos de una letra o una letra seguida de 7 dígitos.
        dni_pattern = re.compile(r'^\d{7}[a-zA-Z]$|^[a-zA-Z]\d{7}$')
        """ # Expresión regular para validar DNI: permite que los dígitos y las letras aparezcan en cualquier orden.
        dni_pattern = re.compile(r'^(?=.*\d)(?=.*[a-zA-Z])[a-zA-Z\d]{8}$')"""
        if not dni_pattern.match(dni):
            raise forms.ValidationError("Ingrese un DNI válido (7 dígitos seguidos de una letra o viceversa).")

        return dni

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        self.validate_birth_date(birth_date)
        return birth_date
    
    def clean_address(self):
        address = self.cleaned_data['address']
        self.validate_length(address, 5, "Ingrese una dirección válida.")
        return address
    
    def clean_email(self):
        email = self.cleaned_data['email']

        # Utiliza el validador de Django para validar la dirección de correo electrónico.
        email_validator = EmailValidator()

        try:
            email_validator(email)
        except forms.ValidationError:
            raise forms.ValidationError("Ingrese una dirección de correo electrónico válida.")

        return email

class ObjetiveForm(forms.ModelForm):

    TIPO = [
        ('VENTAS', 'VENTAS'),
        ('REGISTRO', 'REGISTRO'),
        ('CRISTALES', 'CRISTALES')
    ]

    type = forms.ChoiceField(
        label='Elige tipo de objetivo',
        choices=TIPO,
        required=True,
        widget= forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    class Meta:
        model = Objetives
        fields = ['to', 'type', 'description', 'start_date', 'exp_date', 'quantity']
        widgets = {
            'to': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ejemplo: Peso Argentino',
                    'required':''
                    }
                ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripcion del objetivo',
                    'required':''
                    }
                ),
            'start_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Fecha de inicio',
                    'required':'',
                    'type': 'date'
                    }
                ),
            'exp_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Fecha de finalizacion',
                    'required':'',
                    'type': 'date'
                    }
                ),
            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Cantidad estimada',
                    'required':'',
                }
            )
            }