from django import forms

from .models import Employee
from applications.users.forms import UserCreateForm


class EmployeeForm(UserCreateForm):
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user',]

    def clean_address(self):
        address = self.cleaned_data['address']
        if address and (len(address) < 5):
            raise forms.ValidationError("Ingrese un Direccion válida.")
        return address