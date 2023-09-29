from typing import Any
from django import forms

from .models import *
from applications.core.forms import PersonForm
from applications.core.mixins import ValidationFormMixin


class CustomerForm(PersonForm):
    h_insurance = forms.ModelMultipleChoiceField(
        queryset=HealthInsurance.objects.all(),
        label='Obra Social',
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            insurances = self.instance.customer_insurance.values_list('h_insurance__id', flat=True)
            self.fields['h_insurance'].initial = insurances

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user_made','deleted_at', 'branch']

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        self.validate_birth_date(birth_date)
        return birth_date      
    
class HealthInsuranceForm(ValidationFormMixin):

    name = forms.CharField( 
        label='Nombre',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder' : 'Nombre de la Obra Social',
                   'autofocus': '',
                   'type' : 'text',
                   'pattern': '^[a-zA-Z\s]+$'
                   }
        )
    )

    phone_number = forms.CharField( 
        label='Telefono de contacto',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder' : 'Telefono de contacto',
                   'type' : 'numeric',
                   'pattern' : '[0-9]+'
                   }
        )
    )

    cuit = forms.CharField( 
        label='CUIT',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder' : 'Clave Única de Identificación Tributaria',
                   'type' : 'numeric',
                   'pattern' : '[0-9]+'
                   }
        )
    )

    class Meta:
        model = HealthInsurance
        fields = ['name', 'phone_number', 'cuit']

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

    class Meta:
        model = Correction
        fields = '__all__'
        exclude = ['user_made','deleted_at']

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
            # attrs={'class': 'form-check'}
            )
    )

    class Meta:
        model = Material
        fields = '__all__'
        exclude = ['user_made', 'deleted_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtén la instancia del modelo Material asociada al formulario
        material_instance = self.instance

        # Recorre las opciones de MATERIAL_CHOICES y marca como seleccionada
        # la que corresponde al campo booleano en True en la instancia del modelo
        for choice_value, choice_label in self.fields['material_choice'].choices:
            if getattr(material_instance, choice_value):
                self.fields['material_choice'].initial = choice_value

    def clean(self):
        cleaned_data = super().clean()
        material_choice = cleaned_data.get('material_choice')
    
        cleaned_data[material_choice] = True
        return cleaned_data

class ColorForm(forms.ModelForm):
    COLOR_CHOICES = [
        ('white', 'Blanco'),
        ('full_gray', 'Gris puro'),
        ('gray_gradient', 'Gris gradiente'),
        ('flat_sepia', 'Sepia plana'),
    ]

    color_choice = forms.ChoiceField(
        choices=COLOR_CHOICES,
        required=False,
        label='Color',
        widget=forms.RadioSelect(
            # attrs={'class': 'form-check'}
            )
    )

    class Meta:
        model = Color
        fields = '__all__'
        exclude = ['user_made', 'deleted_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtén la instancia del modelo Material asociada al formulario
        material_instance = self.instance

        # Recorre las opciones de MATERIAL_CHOICES y marca como seleccionada
        # la que corresponde al campo booleano en True en la instancia del modelo
        for choice_value, choice_label in self.fields['color_choice'].choices:
            if getattr(material_instance, choice_value):
                self.fields['color_choice'].initial = choice_value

    def clean(self):
        cleaned_data = super().clean()
        color_choice = cleaned_data.get('color_choice')

        cleaned_data[color_choice] = True
        return cleaned_data

class CristalForm(forms.ModelForm):
    CRISTAL_CHOICES = [
        ('monofocal', 'Monofocal'),
        ('bifocal_fv', 'Bifocal FV'),
        ('bifocal_k', 'Bifocal K'),
        ('bifocal_pi', 'Bifocal PI'),
        ('progressive', 'Progresivo'),
    ]

    cristal_choice = forms.ChoiceField(
        choices=CRISTAL_CHOICES,
        required=False,
        label='Cristal',
        widget=forms.RadioSelect(
            # attrs={'class': 'form-check'}
            )
    )

    class Meta:
        model = Cristal
        fields = '__all__'
        exclude = ['user_made', 'deleted_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtén la instancia del modelo Material asociada al formulario
        material_instance = self.instance

        # Recorre las opciones de MATERIAL_CHOICES y marca como seleccionada
        # la que corresponde al campo booleano en True en la instancia del modelo
        for choice_value, choice_label in self.fields['cristal_choice'].choices:
            if getattr(material_instance, choice_value):
                self.fields['cristal_choice'].initial = choice_value

    def clean(self):
        cleaned_data = super().clean()
        cristal_choice = cleaned_data.get('cristal_choice')

        cleaned_data[cristal_choice] = True
        return cleaned_data

class TratamientForm(forms.ModelForm):
    TRATAMIENT_CHOICES = [
        ('antireflex', 'Antireflex'),
        ('filtro_azul', 'Filtro Azul'),
        ('fotocromatico', 'Fotocromático'),
        ('ultravex', 'Ultravex'),
        ('polarizado', 'Polarizado'),
        ('neutrosolar', 'Neutro Solar'),
    ]

    tratamient_choice = forms.ChoiceField(
        choices=TRATAMIENT_CHOICES,
        required=False,
        label='Tratamiento',
        widget=forms.RadioSelect(
            # attrs={'class': 'form-check'}
            )
    )

    class Meta:
        model = Tratamient
        fields = '__all__'
        exclude = ['user_made', 'deleted_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtén la instancia del modelo Material asociada al formulario
        material_instance = self.instance

        # Recorre las opciones de MATERIAL_CHOICES y marca como seleccionada
        # la que corresponde al campo booleano en True en la instancia del modelo
        for choice_value, choice_label in self.fields['tratamient_choice'].choices:
            if getattr(material_instance, choice_value):
                self.fields['tratamient_choice'].initial = choice_value

    def clean(self):
        cleaned_data = super().clean()
        tratamient_choice = cleaned_data.get('tratamient_choice')

        cleaned_data[tratamient_choice] = True
        return cleaned_data

class InterpupillaryForm(forms.ModelForm):
    cer_od_nanopupilar = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }),
    )

    cer_od_pelicula = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }),
    )

    cer_oi_nanopupilar = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }),
    )

    cer_oi_pelicula = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }),
    )

    cer_total = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }),
    )

    lej_od_nanopupilar = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }),
    )

    lej_od_pelicula = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }),
    )

    lej_oi_nanopupilar = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }),
    )

    lej_oi_pelicula = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }),
    )

    lej_total = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }),
    )

    class Meta:
        model = Interpupillary
        fields = '__all__'
        exclude = ['user_made', 'deleted_at']

class Calibration_OrderForm(forms.ModelForm):

    is_done = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
    )

    armazon = forms.CharField(
        #required=False,
        widget = forms.Textarea(
            attrs={
            'class' : 'form-control',
            'placeholder' : 'Armazon',
            'rows' : '3',
            }
        )
    )

    diagnostic = forms.CharField(
        required=False,
        widget = forms.Textarea(
            attrs={
            'class' : 'form-control',
            'placeholder' : 'Diagnostico',
            'rows' : '3',
            'autofocus' : ''
            }
        )
    )

    observations = forms.CharField(
        required=False,
        widget = forms.Textarea(
            attrs={
            'class' : 'form-control',
            'placeholder' : 'Observaciones',
            'rows' : '3',
            }
        )
    )

    class Meta:
        model = Calibration_Order
        fields = ['is_done','diagnostic', 'armazon', 'observations']

