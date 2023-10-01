from django import forms
from .models import Employee

from applications.users.forms import UserCreateForm, UserUpdateForm
from applications.core.forms import PersonForm
from applications.users.models import User



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
        fields = ('email','first_name', 'last_name','dni', 'phone_code', 'phone_number', 'address')