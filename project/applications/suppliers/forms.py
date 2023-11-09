from django import forms

from .models import Bank, Brand_Supplier, Supplier#, Product_Supplier
from applications.products.models import Brand, Product
from applications.core.mixins import ValidationFormMixin
from django.core.validators import RegexValidator


class SupplierForm(ValidationFormMixin):
    name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'Nombre del proveedor',
                'type': 'text',
                'pattern': '.{3,}',  # Mínimo 3 caracteres
                }
        ),
        validators=[RegexValidator(r'^[a-zA-Z\s]+$', 'El nombre solo puede contener letras y espacios.')]
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
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Telefono de contacto',
                'type': 'number',
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
                'type': 'text',
            }
        ),
    )
    brandsSelected = forms.ModelMultipleChoiceField(
        queryset=Brand.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    banks = forms.ModelMultipleChoiceField(
        queryset=Bank.objects.all(),
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

class BankForm(ValidationFormMixin):

    class Meta:
        model = Bank
        fields = ['cbu', 'bank_name', 'cuit']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = ''

    def clean_bank_name(self):
        name = self.cleaned_data['bank_name']
        name_formated = name.title()
        self.validate_length(name_formated, 3, 'El nombre debe tener al menos 3 caracteres.')
        return name_formated