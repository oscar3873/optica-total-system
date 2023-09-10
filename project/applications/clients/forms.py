from django import forms

from .models import *
from applications.core.forms import PersonForm
from applications.core.mixins import ValidationFormMixin


class CustomerForm(PersonForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user_made','deleted_at']
    
    h_insurence = forms.ModelChoiceField(
        queryset=HealthInsurance.objects.all(),
        label='Obra Social',
        empty_label='Elija una Obra Social',
        required=True,
        widget=forms.Select(attrs={
            'placeholder' : 'Obra Social',
            'class' : 'form-control'
        })
    )
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        self.validate_birth_date(birth_date)
        return birth_date


class HealthInsuranceForm(ValidationFormMixin):
    class Meta:
        model = HealthInsurance
        fields = "__all__"
        exclude = ['user_made','deleted_at']

    name = forms.CharField( 
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    phone_number = forms.CharField( 
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    cuit = forms.CharField( 
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

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

    lej_od_esferico = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    lej_od_cilindrico = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    lej_od_eje = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    lej_oi_esferico = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    lej_oi_cilindrico = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    lej_oi_eje = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    cer_od_esferico = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    cer_od_cilindrico = forms.CharField(
        required=False, 
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    cer_od_eje = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    cer_oi_esferico = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    cer_oi_cilindrico = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    cer_oi_eje = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

class MaterialForm(forms.ModelForm):
    MATERIAL_CHOICES = [
        ('policarbonato', 'Policarbonato'),
        ('organic', 'Organic'),
        ('mineral', 'Mineral'),
        ('m_r8', 'M_R8'),
    ]

    material_choice = forms.ChoiceField(
        choices=MATERIAL_CHOICES,
        required=False,
        label='Material',
        widget=forms.RadioSelect(
            attrs={'class': 'form-check-input'}
        )
    )

    class Meta:
        model = Material
        fields = '__all__'
        exclude = ['user_made', 'deleted_at']

    def clean(self):
        cleaned_data = super().clean()
        material_choice = cleaned_data.get('material_choice')

        if not material_choice:
            raise forms.ValidationError("Debe seleccionar exactamente un campo.")


class ColorForm(forms.ModelForm):
    white = forms.BooleanField(
        required=False,
        label='White',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )
    
    full_gray = forms.BooleanField(
        required=False,
        label='Full Gray',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )
    
    gray_gradient = forms.BooleanField(
        required=False,
        label='Gray Gradient',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )
    
    flat_sepia = forms.BooleanField(
        required=False,
        label='Flat Sepia',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )

    class Meta:
        model = Color
        exclude = ['user_made', 'deleted_at']


class CristalForm(forms.ModelForm):
    monofocal = forms.BooleanField(
        required=False,
        label='Monofocal',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )
    
    bifocal_fv = forms.BooleanField(
        required=False,
        label='Bifocal FV',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )
    bifocal_k = forms.BooleanField(
        required=False,
        label='Bifocal K',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )
    bifocal_pi = forms.BooleanField(
        required=False,
        label='Bifocal PI',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )
    progressive = forms.BooleanField(
        required=False,
        label='Progressive',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )

    class Meta:
        model = Cristal
        exclude = ['user_made', 'deleted_at']


class TratamientForm(forms.ModelForm):
    antireflex = forms.BooleanField(
        required=False,
        label='Antireflex',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
    )
    filtro_azul = forms.BooleanField(
        required=False,
        label='Filtro Azul',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
    )
    fotocromatico = forms.BooleanField(
        required=False,
        label='Fotocromático',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
    )
    ultravex = forms.BooleanField(
        required=False,
        label='Ultravex',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
    )
    polarizado = forms.BooleanField(
        required=False,
        label='Polarizado',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
    )
    neutrosolar = forms.BooleanField(
        required=False,
        label='Neutro Solar',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
    )

    class Meta:
        model = Tratamient
        exclude = ['user_made', 'deleted_at']


class InterpupillaryForm(forms.ModelForm):
    cer_od_nanopupilar = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    cer_od_pelicula = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    cer_oi_nanopupilar = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    cer_oi_pelicula = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    cer_total = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    lej_od_nanopupilar = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    lej_od_pelicula = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    lej_oi_nanopupilar = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    lej_oi_pelicula = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    lej_total = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Interpupillary
        fields = '__all__'
        exclude = ['user_made', 'deleted_at']


class Calibration_OrderForm(forms.ModelForm):
    class Meta:
        model = Calibration_Order
        fields = ['is_done','diagnostic', 'armazon', 'observations']

