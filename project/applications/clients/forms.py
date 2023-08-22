from django import forms
from .models import *

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


class CorrectionForm(forms.ModelForm):
    class Meta:
        model = Correction
        fields = ['lej_od_esferico', 'lej_od_cilindrico', 'lej_od_eje', 'lej_oi_esferico', 'lej_oi_cilindrico', 'lej_oi_eje', 'cer_od_esferico', 'cer_od_cilindrico', 'cer_od_eje', 'cer_oi_esferico', 'cer_oi_cilindrico', 'cer_oi_eje']

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['policarbonato', 'organic', 'mineral', 'm_r8']

class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ['white', 'full_gray', 'gray_gradient', 'flat_sepia']

class CristalForm(forms.ModelForm):
    class Meta:
        model = Cristal
        fields = ['monofocal', 'bifocal_fv', 'bifocal_k', 'bifocal_pi', 'progressive']

class TratamientForm(forms.ModelForm):
    class Meta:
        model = Tratamient
        fields = ['antireflex', 'filtro_azul', 'fotocromatico', 'ultravex', 'polarizado', 'neutrosolar']

class InterpupillaryForm(forms.ModelForm):
    class Meta:
        model = Interpupillary
        fields = ['lej_od_nanopupilar', 'lej_od_pelicula', 'lej_oi_nanopupilar', 'lej_oi_pelicula', 'lej_total', 'cer_od_nanopupilar', 'cer_od_pelicula', 'cer_oi_nanopupilar', 'cer_oi_pelicula', 'cer_total']

class CalibrationOrderForm(forms.ModelForm):
    lejos_od_esferico = forms.CharField(max_length=10, required=False)
    lej_od_cilindrico = forms.CharField(max_length=10, required=False)
    lej_od_eje = forms.CharField(max_length=10, required=False)
    lej_oi_esferico = forms.CharField(max_length=10, required=False)
    lej_oi_cilindrico = forms.CharField(max_length=10, required=False)
    lej_oi_eje = forms.CharField(max_length=10, required=False)
    cer_od_esferico = forms.CharField(max_length=10, required=False)
    cer_od_cilindrico = forms.CharField(max_length=10, required=False)
    cer_od_eje = forms.CharField(max_length=10, required=False)
    cer_oi_esferico = forms.CharField(max_length=10, required=False)
    cer_oi_cilindrico = forms.CharField(max_length=10, required=False)
    cer_oi_eje = forms.CharField(max_length=10, required=False)
    
    policarbonato = forms.BooleanField(required=False)
    organic = forms.BooleanField(required=False)
    mineral = forms.BooleanField(required=False)
    m_r8 = forms.BooleanField(required=False)
    
    white = forms.BooleanField(required=False)
    full_gray = forms.BooleanField(required=False)
    gray_gradient = forms.BooleanField(required=False)
    flat_sepia = forms.BooleanField(required=False)
    
    monofocal = forms.BooleanField(required=False)
    bifocal_fv = forms.BooleanField(required=False)
    bifocal_k = forms.BooleanField(required=False)
    bifocal_pi = forms.BooleanField(required=False)
    progressive = forms.BooleanField(required=False)
    
    antireflex = forms.BooleanField(required=False)
    filtro_azul = forms.BooleanField(required=False)
    fotocromatico = forms.BooleanField(required=False)
    ultravex = forms.BooleanField(required=False)
    polarizado = forms.BooleanField(required=False)
    neutrosolar = forms.BooleanField(required=False)
    
    lej_od_nanopupilar = forms.CharField(max_length=10, required=False)
    lej_od_pelicula = forms.CharField(max_length=10, required=False)
    lej_oi_nanopupilar = forms.CharField(max_length=10, required=False)
    lej_oi_pelicula = forms.CharField(max_length=10, required=False)
    lej_total = forms.CharField(max_length=10, required=False)
    cer_od_nanopupilar = forms.CharField(max_length=10, required=False)
    cer_od_pelicula = forms.CharField(max_length=10, required=False)
    cer_oi_nanopupilar = forms.CharField(max_length=10, required=False)
    cer_oi_pelicula = forms.CharField(max_length=10, required=False)
    cer_total = forms.CharField(max_length=10, required=False)
    
    class Meta:
        model = Calibration_Order
        fields = ['is_done','medical_details', 'employees', 'armazon', 'observations']
