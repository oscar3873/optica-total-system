from django import forms
from .models import Customer, MedicalHistory, HealthInsurance

def validate_length(field_value, min_length, error_message):
    if field_value and len(field_value) < min_length:
        raise forms.ValidationError(error_message)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

    def clean_address(self):
        address = self.cleaned_data['address']
        validate_length(address, 5, "Ingrese una dirección válida.")
        return address


class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['diagnostic',]

    def clean_diagnostic(self):
        diagnostic = self.cleaned_data['diagnostic']
        validate_length(diagnostic, 5, "Ingrese un diagnóstico válido.")
        return diagnostic


class HealthInsuranceForm(forms.ModelForm):
    class Meta:
        model = HealthInsurance
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data['name']
        validate_length(name, 3, "El nombre de la sucursal debe contener al menos 3 caracteres.")
        return name

    def clean_cuit(self):
        cuit = self.cleaned_data['cuit']
        cuit_str = str(cuit)
        validate_length(cuit_str, 10, "Ingrese un CUIT válido.")
        return cuit


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

    def clean_address(self):
        address = self.cleaned_data['address']
        validate_length(address, 5, "Ingrese una dirección válida.")
        return address


class MedicalHistoryUpdateForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['diagnostic',]

    def clean_diagnostic(self):
        diagnostic = self.cleaned_data['diagnostic']
        validate_length(diagnostic, 5, "Ingrese un diagnóstico válido.")
        return diagnostic


class HealthInsuranceUpdateForm(forms.ModelForm):
    class Meta:
        model = HealthInsurance
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data['name']
        validate_length(name, 3, "El nombre debe contener al menos 3 caracteres.")
        return name

    def clean_cuit(self):
        cuit = self.cleaned_data['cuit']
        cuit_str = str(cuit)
        validate_length(cuit_str, 10, "Ingrese un CUIT válido.")
        return cuit
