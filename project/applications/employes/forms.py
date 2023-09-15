from django import forms
from .models import Employee

from applications.users.forms import UserCreateForm,UserUpdateForm
""" class EmployeeForm(UserCreateForm):

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
 """
class EmployeeCreateForm(UserCreateForm):
    employment_date = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
            },
            format='%Y-%m-%d'
        )
    )
    class Meta:
        model = Employee
        fields = ['employment_date',]


    def clean_employment_date(self):
        employment_date = self.cleaned_data.get('employment_date')
        self.validate_date(employment_date)
        return employment_date




from django import forms
from django.core.validators import RegexValidator 
from applications.core.models import Person
from applications.users.models import User, Employee
from applications.core.mixins import ValidationFormMixin  # Asegúrate de importar los validadores necesarios

class EmployeeUpdateForm(UserUpdateForm):
    # Campos de Person


    # Campos de Employee
    employment_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
            },
            format='%Y-%m-%d'
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance.pk:
            # Rellenar los campos de User y Person con los datos existentes
            
            self.fields['employment_date'].initial = self.instance.employment_date
            
    class Meta:
        model = Employee
        fields = ['last_name','email','first_name','dni','phone_number','address']
