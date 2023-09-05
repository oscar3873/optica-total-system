from django import forms

from .models import *
from applications.core.mixins import ValidationFormMixin


class CustomerForm(ValidationFormMixin):

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    phone_number = forms.IntegerField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )
    
    dni = forms.IntegerField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type':'date',
                   'class': 'form-control datetimepicker'
                   }
        )
    )

    email = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )


    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user_made','deleted_at']

    def clean_address(self):
        address = self.cleaned_data['address']
        self.validate_length(address, 5, "Ingrese una dirección válida.")
        return address
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        self.validate_birth_date(birth_date)
        return birth_date


class HealthInsuranceForm(ValidationFormMixin):
    class Meta:
        model = HealthInsurance
        fields = "__all__"
        exclude = ['user_made','deleted_at']

    def clean_name(self):
        name = self.cleaned_data['name']
        self.validate_length(name, 3, "El nombre de la sucursal debe contener al menos 3 caracteres.")
        return name

    def clean_cuit(self):
        cuit = self.cleaned_data['cuit']
        cuit_str = str(cuit)
        self.validate_length(cuit_str, 10, "Ingrese un CUIT válido.")
        return cuit


class CorrectionForm(forms.ModelForm):
    class Meta:
        model = Correction
        fields = '__all__'
        exclude = ['user_made','deleted_at']

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        exclude = ['user_made', 'deleted_at']
        widgets = {
            'policarbonato': forms.CheckboxInput,
            'organic': forms.CheckboxInput,
            'mineral': forms.CheckboxInput,
            'm_r8': forms.CheckboxInput,
        }

class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        exclude = ['user_made', 'deleted_at']
        widgets = {
            'white': forms.CheckboxInput,
            'full_gray': forms.CheckboxInput,
            'gray_gradient': forms.CheckboxInput,
            'flat_sepia': forms.CheckboxInput,
        }

class CristalForm(forms.ModelForm):
    class Meta:
        model = Cristal
        exclude = ['user_made', 'deleted_at']
        widgets = {
            'monofocal': forms.CheckboxInput,
            'bifocal_fv': forms.CheckboxInput,
            'bifocal_k': forms.CheckboxInput,
            'bifocal_pi': forms.CheckboxInput,
            'progressive': forms.CheckboxInput,
        }

class TratamientForm(forms.ModelForm):
    class Meta:
        model = Tratamient
        exclude = ['user_made', 'deleted_at']
        widgets = {
            'antireflex': forms.CheckboxInput,
            'filtro_azul': forms.CheckboxInput,
            'fotocromatico': forms.CheckboxInput,
            'ultravex': forms.CheckboxInput,
            'polarizado': forms.CheckboxInput,
            'neutrosolar': forms.CheckboxInput,
        }

class InterpupillaryForm(forms.ModelForm):
    class Meta:
        model = Interpupillary
        fields = '__all__'
        exclude = ['user_made','deleted_at']

class Calibration_OrderForm(forms.ModelForm):
    class Meta:
        model = Calibration_Order
        fields = ['is_done','diagnostic', 'armazon', 'observations']

