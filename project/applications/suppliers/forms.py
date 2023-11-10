from django import forms

from .models import *
from applications.products.models import Brand
from applications.core.mixins import ValidationFormMixin


class SupplierForm(ValidationFormMixin):
    name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'Nombre del proveedor',
                }
        ),
    )

    PHONE_CODE_CHOICES = (
        ('+54', '+54'),
        ('+56', '+56'),
        ('+591', '+591'),
        # Agrega más opciones según tus necesidades
    )

    phone_code = forms.ChoiceField(
        label='Código de país',
        choices=PHONE_CODE_CHOICES,
        required=True,  # Puede ser opcional
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

    phone_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Telefono de contacto',
                'class':'form-control'
                }
        )
    )
    email=forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Correo electrónico',
                'class':'form-control'
                }
        )
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'Domicilio',
            }
        ),
    )
    brandsSelected = forms.ModelMultipleChoiceField(
        queryset=Brand.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    cbu = forms.ModelMultipleChoiceField(
        queryset=Cbu.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    
    class Meta:
        model = Supplier
        fields = ('name', 'phone_number', 'phone_code', 'email', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:  # Update
            related_brands = self.instance.brand_suppliers.values_list('brand__id', flat=True)
            self.fields['brandsSelected'].initial = related_brands

    def clean_name(self):
        name = self.cleaned_data['name']
        name_formated = name.title()
        self.validate_length(name_formated, 3, 'El nombre del proveedor debe tener al menos 3 carácteres.')
        return name_formated

class CBUForm(ValidationFormMixin):

    class Meta:
        model = Cbu
        fields = ['bank', 'cbu', 'cuit']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = ''

        self.fields['bank'].queryset = Bank.objects.all()


class BankForm(ValidationFormMixin):
    bank_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'Ej: Banco Nación',
            }
        ),
    )

    class Meta:
        model = Bank
        fields = ['bank_name',]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = ''
            
    def clean_bank_name(self):
        name = self.cleaned_data['bank_name']
        name_formated = name.capitalize()
        self.validate_length(name_formated, 3, 'El nombre debe tener al menos 3 caracteres.')

        return name_formated