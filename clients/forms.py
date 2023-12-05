from typing import Any
from django import forms


from .models import *
from core.forms import PersonForm
from core.mixins import ValidationFormMixin
from products.models import Product


class CustomerForm(PersonForm):
    h_insurance = forms.ModelMultipleChoiceField(
        queryset=HealthInsurance.objects.all(),
        label='Obra Social',
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
        })
    )

    has_credit_account = forms.BooleanField(
        label='¿Tiene una cuenta corriente?',
        required=False,
        widget= forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for index, field in self.fields.items():
            field.required = True
        self.fields['has_credit_account'].required = False
        self.fields['h_insurance'].required = False
        self.fields['address'].required = False
        self.fields['email'].required = False
        self.fields['birth_date'].required = False

        if self.instance.pk:
            insurances = self.instance.customer_insurance.values_list('h_insurance__id', flat=True)
            self.fields['h_insurance'].initial = insurances

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user_made','deleted_at', 'branch', 'credit_balance']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            email = None
        return email


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

    phone_number = forms.IntegerField( 
        label='Telefono de contacto',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder' : 'Telefono de contacto',
                }
        )
    )

    cuit = forms.IntegerField( 
        label='CUIT',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder' : 'Clave Única de Identificación Tributaria',
                }
        )
    )

    class Meta:
        model = HealthInsurance
        fields = ['name', 'phone_number', 'cuit']

    def clean_name(self):
        name = self.cleaned_data['name']
        self.validate_length(name, 3, "El nombre de la sucursal debe contener al menos 3 caracteres.")
        return name.title()

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
    class Meta:
        model = Material
        fields = '__all__'
        exclude = ['user_made', 'deleted_at']
        widgets = {
            'policarbonato': forms.CheckboxInput(attrs={'required': False}),
            'organic': forms.CheckboxInput(attrs={'required': False}),
            'mineral': forms.CheckboxInput(attrs={'required': False}),
            'm_r8': forms.CheckboxInput(attrs={'required': False}),
        }

class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = '__all__'
        exclude = ['user_made', 'deleted_at']
        widgets = {
            'white': forms.CheckboxInput(attrs={'required': False}),
            'full_gray': forms.CheckboxInput(attrs={'required': False}),
            'gray_gradient': forms.CheckboxInput(attrs={'required': False}),
            'flat_sepia': forms.CheckboxInput(attrs={'required': False}),
        }

class CristalForm(forms.ModelForm):
    class Meta:
        model = Cristal
        fields = '__all__'
        exclude = ['user_made', 'deleted_at']
        widgets = {
            'monofocal': forms.CheckboxInput(attrs={'required': False}),
            'bifocal_fv': forms.CheckboxInput(attrs={'required': False}),
            'bifocal_k': forms.CheckboxInput(attrs={'required': False}),
            'bifocal_pi': forms.CheckboxInput(attrs={'required': False}),
            'progressive': forms.CheckboxInput(attrs={'required': False}),
        }

class TratamientForm(forms.ModelForm):
    class Meta:
        model = Tratamient
        fields = '__all__'
        exclude = ['user_made', 'deleted_at']
        widgets = {
            'antireflex': forms.CheckboxInput(attrs={'required': False}),
            'filtro_azul': forms.CheckboxInput(attrs={'required': False}),
            'fotocromatico': forms.CheckboxInput(attrs={'required': False}),
            'ultravex': forms.CheckboxInput(attrs={'required': False}),
            'polarizado': forms.CheckboxInput(attrs={'required': False}),
            'neutrosolar': forms.CheckboxInput(attrs={'required': False}),
        }


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

class ServiceOrderForm(forms.ModelForm):
    armazon = forms.ModelChoiceField(
        required = False,
        queryset = Product.objects.filter(category__name__icontains='Armazon'),
        widget = forms.Select(
            attrs={
                'class': 'form-control',
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
        model = ServiceOrder
        fields = ['diagnostic', 'armazon', 'observations']

    def __init__(self, *args, **kwargs):
        armazon = kwargs.pop('kwargs', None)
        super().__init__(*args, **kwargs)

        if armazon:
            self.fields['armazon'].queryset = armazon
            self.fields['armazon'].initial = armazon