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

    jornada = forms.CharField(
        max_length= 50,
        required=False,
        widget= forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Employee
        fields = ['employment_date', 'jornada']

    def clean_employment_date(self):
        employment_date = self.cleaned_data.get('employment_date')
        self.validate_date(employment_date)
        return employment_date
    
    def clean_jornada(self):
        jornada = self.cleaned_data.get('jornada')
        self.validate_length(jornada, 4, 'Debe contener por lo menos 4 carácteres.')
        return jornada
    
    
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

    jornada = forms.CharField(
        max_length= 50,
        required=False,
        widget= forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Employee
        fields = ('employment_date', 'jornada')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['dni'].initial = self.instance.user.dni
        self.fields['address'].initial = self.instance.user.address
        self.fields['phone_code'].initial = self.instance.user.phone_code
        self.fields['phone_number'].initial = self.instance.user.phone_number
        self.fields['birth_date'].initial = self.instance.user.birth_date

        self.fields['email'].required = False
    
    def clean_jornada(self):
        jornada = self.cleaned_data.get('jornada')
        self.validate_length(jornada, 4, 'Debe contener por lo menos 4 carácteres.')
        return jornada