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

    lej_od_esferico = forms.CharField( 
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    lej_od_cilindrico = forms.CharField( 
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    lej_od_eje = forms.CharField( 
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    lej_oi_esferico = forms.CharField( 
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    lej_oi_cilindrico = forms.CharField( 
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    lej_oi_eje = forms.CharField( 
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    cer_od_esferico = forms.CharField( 
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    cer_od_cilindrico = forms.CharField( 
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    cer_od_eje = forms.CharField( 
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    cer_oi_esferico = forms.CharField( 
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    cer_oi_cilindrico = forms.CharField( 
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    cer_oi_eje = forms.CharField( 
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

class MaterialForm(forms.ModelForm):

    policarbonato = forms.BooleanField(
        label='Policarbonato',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )
    
    organic = forms.BooleanField(
        label='Organic',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )
    
    mineral = forms.BooleanField(
        label='Mineral',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )
    
    m_r8 = forms.BooleanField(
        label='M_R8',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )


    class Meta:
        model = Material
        exclude = ['user_made', 'deleted_at']

    def clean(self):  ### CONSULTAR
        cleaned_data = super().clean()
        selected_fields = [field for field in self.fields if self.cleaned_data.get(field)]
        if len(selected_fields) != 1:
            raise forms.ValidationError("Debe seleccionar exactamente un campo.")


class ColorForm(forms.ModelForm):
    white = forms.BooleanField(
        label='White',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )
    
    full_gray = forms.BooleanField(
        label='Full Gray',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )
    
    gray_gradient = forms.BooleanField(
        label='Gray Gradient',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )
    
    flat_sepia = forms.BooleanField(
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
        label='Monofocal',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )
    
    bifocal_fv = forms.BooleanField(
        label='Bifocal FV',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )
    bifocal_k = forms.BooleanField(
        label='Bifocal K',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )
    bifocal_pi = forms.BooleanField(
        label='Bifocal PI',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
        )
    progressive = forms.BooleanField(
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
        label='Antireflex',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
    )
    filtro_azul = forms.BooleanField(
        label='Filtro Azul',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
    )
    fotocromatico = forms.BooleanField(
        label='Fotocromático',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
    )
    ultravex = forms.BooleanField(
        label='Ultravex',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
    )
    polarizado = forms.BooleanField(
        label='Polarizado',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
    )
    neutrosolar = forms.BooleanField(
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
    class Meta:
        model = Interpupillary
        fields = '__all__'
        exclude = ['user_made', 'deleted_at']
        widgets = {
            'lej_od_nanopupilar': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'lej_od_pelicula': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'lej_oi_nanopupilar': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'lej_oi_pelicula': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'lej_total': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'cer_od_nanopupilar': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'cer_od_pelicula': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'cer_oi_nanopupilar': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'cer_oi_pelicula': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'cer_total': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
        }
 

class Calibration_OrderForm(forms.ModelForm):
    class Meta:
        model = Calibration_Order
        fields = ['is_done','diagnostic', 'armazon', 'observations']

