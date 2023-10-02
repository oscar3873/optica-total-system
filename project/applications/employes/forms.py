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
    
    
class EmployeeUpdateForm(PersonForm):
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
        fields = ('employment_date', )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['dni'].initial = self.instance.user.dni
        self.fields['address'].initial = self.instance.user.address
        self.fields['phone_code'].initial = self.instance.user.phone_code
        self.fields['phone_number'].initial = self.instance.user.phone_number
        self.fields['email'].initial = self.instance.user.email
        self.fields['birth_date'].initial = self.instance.user.birth_date

        self.fields['email'].required = False