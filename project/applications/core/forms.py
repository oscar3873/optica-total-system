import re
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
        required = False,
        widget = forms.TextInput(attrs={
            'placeholder' : 'DNI',
            'class' : 'form-control',
            'type' : 'text',
        }),
        validators=[
            RegexValidator(
                r'^(?:[FMfm]?\d{1,10}|\d{1,10})$',
                'Ingrese un DNI válido (hasta 8 dígitos numéricos o precedidos por "F" o "M").',
                'invalid_dni'
            )
        ]
    )

    address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder' : 'Domicilio',
            'class' : 'form-control',
            'type' : 'text',
            }),
    )
    PHONE_CODE_CHOICES = (
        ('+54', '+54'),
        ('+56', '+56'),
        ('+591', '+591'),
        # Agrega más opciones según tus necesidades
    )

    phone_code = forms.ChoiceField(
        label='Código de país',
        choices=PHONE_CODE_CHOICES,
        required=False,  # Puede ser opcional
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

    phone_number = forms.IntegerField(
        required = False,
        widget = forms.TextInput(attrs={
            'placeholder' : 'Telefono de contacto',
            'class' : 'form-control',
            'type' : 'numeric',
            'pattern' : '[0-9]+'
        }),
    )

    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'placeholder': 'Fecha de Nacimiento',
                'type': 'date',
                'class': 'form-control'
            },
            format='%Y-%m-%d',
        )
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder' : 'Correo electrónico',
            'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Person
        fields = ["first_name","last_name","dni","address","email","phone_code","phone_number","birth_date"]

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
        if phone_number:
            self.validate_length(phone_number, 6, "Ingrese un número de teléfono válido.")
            phone_number_pattern = re.compile(r'^(?:\+?[0-9]{1,3})?[0-9]{6,}$')

            if not phone_number_pattern.match(str(phone_number)):
                raise forms.ValidationError("Ingrese un número de teléfono válido.")
        return phone_number
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        self.validate_birth_date(birth_date)
        return birth_date
    
    def clean_address(self):
        address = self.cleaned_data['address']
        if address:
            self.validate_length(address, 5, "Ingrese una dirección válida.")
        return address
    
    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if dni:
            self.validate_length(dni, 6, "Ingrese una DNI válida.")
        return dni
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
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
        


class ObjetiveForm(ValidationFormMixin):
    PARA= [
        ('EMPLEADOS', 'EMPLEADOS'),
        ('SUCURSAL', 'SUCURSAL'),
    ]

    TIPO = [
        ('VENTA', 'VENTA'),
    ]

    to = forms.ChoiceField(
        choices=PARA,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    tipo = forms.ChoiceField(
        choices=TIPO,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    description = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    start_date = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        )
    )
    exp_date = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        )
    )
    quantity = forms.IntegerField(
        min_value=1,
        max_value=9999999999,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Objetives
        fields = ['to', 'title', 'description', 'start_date', 'exp_date', 'quantity']

    def clean_title(self):
        title = self.cleaned_data['title']
        self.validate_length(title, 3, "El Titulo debe contener al menos 3 carácteres.")
        return title.title()
    
    def clean_description(self):
        description = self.cleaned_data['description']
        self.validate_length(description, 3, "La Descripcion debe contener al menos 3 carácteres.")
        return description.title()

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity and quantity <= 0:
            raise forms.ValidationError("Ingrese una Cantidad válida.")
        return quantity

    def clean(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['exp_date']
        if start_date and end_date and start_date < end_date:
            raise forms.ValidationError("La Fecha de Finalizacion no puede ser anterior a la Fecha de Inicio.")
        return self.cleaned_data
