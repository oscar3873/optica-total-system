from django import forms
from .models import Employee

from applications.users.forms import UserCreateForm
class EmployeeForm(UserCreateForm):

    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type':'date'}
        ),
        required=False
    )
    class Meta:
        model = Employee
        fields = ['phone_number', 'birth_date', 'dni', 'address',]

    def clean_address(self):
        address = self.cleaned_data['address']
        self.validate_length(address, 5, 'La dirección debe tener 5 caracter')
        return address
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        self.validate_birth_date(birth_date)
        return birth_date


