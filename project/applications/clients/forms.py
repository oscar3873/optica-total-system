from django import forms
from .models import Customer, Customer_HealthInsurance, MedicalHistory

from applications.core.forms import PersonForm

class CustomerForm(PersonForm):
    address = forms.CharField(
        max_length=150,
        label='Direccion',
        widget=forms.TextInput(attrs={'placeholder': 'Direccion'}),
        min_length= 4 
    )

    class Meta:
        model = Customer
        fields = ['address',]


class MedicalHistoryForm(forms.ModelForm):


    class Meta:
        model = MedicalHistory
        fields = '__all__'