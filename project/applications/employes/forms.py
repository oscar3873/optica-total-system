from django import forms
from .models import Employee
from applications.core.forms import PersonForm

class EmployeeCreateForm(PersonForm):

    address = forms.CharField(
        max_length=120,
        label='Dirección',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Dirección'}),
    )

    class Meta:
        model = Employee
        fields = ['from_branch','address']


    def clean_address(self):
        address = self.cleaned_data['address']
        if address and (len(address) < 5):
            raise forms.ValidationError("Ingrese un Direccion válida.")
        return address