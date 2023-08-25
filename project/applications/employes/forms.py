from datetime import timedelta
from django import forms
from project.settings.base import DATE_NOW
from .models import Employee
from applications.users.forms import UserCreateForm

################################################################
def validate_length(field_value, min_length, error_message):
    """
    Valida longitud de una cadena.
        Para nombres, apellidos, direcciones, telefonos, etc.
        Muestra el error mandado por argumento.
    """
    if field_value and len(field_value) < min_length:
        raise forms.ValidationError(error_message)

def validate_birth_date(birth_date):
    """
    Valida fecha de nacimiento.
        Debe tener por lo menos 3 meses de vida o no superar los 85 años.
    """
    if birth_date and birth_date >= DATE_NOW.date() - timedelta(days=90):
        raise forms.ValidationError('La fecha establecida no puede registrarse.')

    age_limit = DATE_NOW.date() - timedelta(days=85*365)
    if birth_date and birth_date <= age_limit:
        raise forms.ValidationError('La fecha establecida no puede superar los 85 años.')
################################################################

class EmployeeForm(UserCreateForm):

    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type':'date'}
        )
    )
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user','user_made']

    def clean_address(self):
        address = self.cleaned_data['address']
        validate_length(address, 5, 'La dirección debe tener 5 caracter')
        return address
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        validate_birth_date(birth_date)
        return birth_date

