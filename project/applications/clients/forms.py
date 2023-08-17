from django import forms
from .models import Customer, Customer_HealthInsurance, MedicalHistory

from .models import HealthInsurance

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

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
    

class HealthInsuranceForm(forms.ModelForm):
    name = forms.CharField(
        max_length=250,
        min_length=3,
        required=True,
        label='Nombre de Sucursal',
        widget=forms.TextInput(attrs={'placeholder': 'Sucursal'}),
    )

    cuit = forms.IntegerField(
        required=True,
        label='CUIT',
        widget=forms.TextInput(attrs={'placeholder': 'CUIT'}),
    )

    class Meta:
        model = HealthInsurance
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data['name']
        if name and len(name) < 3:
            raise forms.ValidationError("El nombre de la sucursal debe contener minimo 4 caracteres.")
        return name

    def clean_cuit(self):
        cuit = self.cleaned_data['cuit']
        cuit_str = str(cuit)
        if cuit and len(cuit_str) < 10:
            raise forms.ValidationError("Ingrese un CUIT válido.")
        return cuit
