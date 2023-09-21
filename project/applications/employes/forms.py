from django import forms
from .models import Employee

from applications.users.forms import UserCreateForm, UserUpdateForm
from applications.core.forms import PersonForm
from applications.users.models import User


class EmployeeUpdateForm(PersonForm):
    class Meta:
        model = Employee
        fields = ('email','first_name', 'last_name','dni', 'phone_code', 'phone_number', 'address')

class EmployeeCreateForm(UserCreateForm):
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
    class Meta:
        model = Employee
        fields = ['employment_date',]

    def clean_employment_date(self):
        employment_date = self.cleaned_data.get('employment_date')
        self.validate_date(employment_date)
        return employment_date
    
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
        
        # if self.instance.pk:
        #     # Rellenar los campos de User y Person con los datos existentes
        #     self.fields['employment_date'].initial = self.instance.employment_date
            
    class Meta:
        model = User
        fields = ['last_name','email','first_name','dni','phone_number','address', 'birth_date']
