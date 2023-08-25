from datetime import timedelta
from django import forms

from project.settings.base import DATE_NOW

from .models import Person


################################################################
def validate_length(field_value, min_length, error_message):
    """
    Valida longitud de una cadena.
        Para nombres, apellidos, direcciones, telefonos, etc.
        Muestra el error mandado por argumento.
    """
    field_value = str(field_value)
    if field_value and len(field_value) < min_length:
        raise forms.ValidationError(error_message)

def validate_birth_date(birth_date):
    """
    Valida fecha de nacimiento.
        Debe tener por lo menos 3 meses de vida o no superar los 85 años.
    """
    if birth_date and birth_date >= DATE_NOW.date() - timedelta(days=30):
        raise forms.ValidationError('La fecha establecida no puede registrarse.')

    age_limit = DATE_NOW.date() - timedelta(days=85*365)
    if birth_date and birth_date <= age_limit:
        raise forms.ValidationError('La fecha establecida no puede superar los 85 años.')
################################################################

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data['first_name']
        validate_length(name, 3, "Ingrese un nombre válido.")
        return name
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        validate_length(last_name, 3, "Ingrese un apellido válido.")
        return last_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        validate_length(phone_number, 9, "Ingrese un número de teléfono válido")
        return phone_number

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        validate_length(dni, 7, "Ingrese un número de DNI válido.")
        return dni

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        validate_birth_date(birth_date)
        return birth_date