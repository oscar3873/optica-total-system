from django import forms
from .models import Customer, Customer_HealthInsurance, MedicalHistory

from applications.core.forms import PersonForm

class CustomerForm(PersonForm):
    address = forms.CharField(
        max_length=150,
        label='Direccion',
        widget=forms.TextInput(attrs={'placeholder': 'Direccion'}),
    )

    class Meta:
        model = Customer
        fields = ['address',]


    def clean_address(self):
        address = self.cleaned_data['address']
        if address and (len(address) < 5):
            raise forms.ValidationError("Ingrese un Direccion válida.")
        return address


class MedicalHistoryForm(forms.ModelForm):
    diagnostic = forms.CharField(
        max_length=250,
        label='Diagnostico',
        widget=forms.TextInput(attrs={'placeholder': 'Diagnostico'}),
    )

    class Meta:
        model = MedicalHistory
        fields = '__all__'

    def clean_diagnostic(self):
        diagnostic = self.cleaned_data['diagnostic']
        if diagnostic and (len(diagnostic) < 5):
            raise forms.ValidationError("Ingrese un Diagnostico válido.")
        return diagnostic