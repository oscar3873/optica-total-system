from django import forms

from .models import Supplier, Product_Supplier
from applications.products.models import Product
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
    email=forms.CharField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Correo electrónico',
                'type': 'email',
                'pattern': '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                'class':'form-control'
                }
        )
    )
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
        )
    class Meta:
        model = Supplier
        fields = ('name','phone_number','phone_code','email','products',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Update
            related_products = self.instance.product_suppliers.values_list('product__id', flat=True)
            available_products = Product.objects.exclude(id__in=related_products) | Product.objects.filter(id__in=related_products)
            self.fields['products'].queryset = available_products
            self.fields['products'].initial = related_products
        else:  # Create
            all_products = Product.objects.all()
            related_products = Product_Supplier.objects.values_list('product__id', flat=True)
            available_products = all_products.exclude(id__in=related_products)
            self.fields['products'].queryset = available_products

    def clean_name(self):
        name = self.cleaned_data['name']
        self.validate_length(name, 3, 'El nombre del proveedor debe tener al menos 3 carácteres.')
        return name
    

    """ def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']

        # Expresión regular para validar números de teléfono de varios países.
        phone_number_pattern = re.compile(r'^(?:\+?[0-9]{1,3})?[0-9]{6,}$')

        if not phone_number_pattern.match(str(phone_number)):
            raise forms.ValidationError("Ingrese un número de teléfono válido.")

        return phone_number
    """
    """ def clean_email(self):
        email = self.cleaned_data['email']

        # Utiliza el validador de Django para validar la dirección de correo electrónico.
        email_validator = EmailValidator()

        try:
            email_validator(email)
        except forms.ValidationError:
            raise forms.ValidationError("Ingrese una dirección de correo electrónico válida.")

        return email
"""
