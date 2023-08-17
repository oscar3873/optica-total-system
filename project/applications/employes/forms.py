from django import forms
from .models import Employee
from applications.core.forms import PersonForm
from applications.users.forms import UserCreateForm

from django.core.validators import RegexValidator


class EmployeeCreateForm(UserCreateForm, PersonForm):

    address = forms.CharField(
        max_length=120,
        label='Dirección',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Dirección'}),
    )

    class Meta:
        model = Employee
        fields = ['from_branch','address']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].required = False  # Cambiar a True si es requerido
        self.fields['password2'].required = False  # Cambiar a True si es requerido


    def clean_address(self):
        address = self.cleaned_data['address']
        if address and (len(address) < 5):
            raise forms.ValidationError("Ingrese un Direccion válida.")
        return address