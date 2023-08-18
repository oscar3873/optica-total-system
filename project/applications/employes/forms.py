from datetime import timedelta
from django import forms
from project.settings.base import DATE_NOW
from .models import Employee
from applications.users.forms import UserCreateForm


class EmployeeForm(UserCreateForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type':'date'}
        )
    )

    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user',]

    def clean_address(self):
        address = self.cleaned_data['address']
        if address and (len(address) < 5):
            raise forms.ValidationError("Ingrese un Direccion válida.")
        return address
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        validate_birth_date(birth_date)
        return birth_date

class EmployeeUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type':'date'}
        )
    )

    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user',]

    def clean_address(self):
        address = self.cleaned_data['address']
        if address and (len(address) < 5):
            raise forms.ValidationError("Ingrese un Direccion válida.")
        return address
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        validate_birth_date(birth_date)
        return birth_date


def validate_birth_date(birth_date):
    if birth_date and birth_date >= DATE_NOW.date() - timedelta(days=30):
        raise forms.ValidationError('La fecha establecida no puede registrarse.')

    age_limit = DATE_NOW.date() - timedelta(days=85*365)
    if birth_date and birth_date <= age_limit:
        raise forms.ValidationError('La fecha establecida no puede superar los 85 años.')
