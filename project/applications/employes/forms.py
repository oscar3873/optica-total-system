from django import forms
from .models import Employee
from applications.users.forms import UserCreateForm

from applications.core.forms import ValidationFormMixin

class EmployeeForm(UserCreateForm, ValidationFormMixin):

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
        self.validate_length(address, 5, 'La dirección debe tener 5 caracter')
        return address
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        self.validate_birth_date(birth_date)
        return birth_date

