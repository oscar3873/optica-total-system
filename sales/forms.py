from django import forms

from core.mixins import ValidationFormMixin
from products.models import Product
from .models import *

class SaleForm(forms.ModelForm):
    description = forms.CharField(
        required = False,
        widget = forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    amount = forms.DecimalField(
        required = False,
        widget = forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )

    customer = forms.ModelChoiceField(
        required=False,
        queryset = Customer.objects.all(),
        widget = forms.RadioSelect()
    )

    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    discount = forms.IntegerField(
        required=False,
        initial = 0,
        widget = forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    
    class Meta:
        model = Sale
        fields = ['customer', 'discount']


class OrderDetailForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        required=False,
        queryset=Product.objects.all(),
        widget=forms.RadioSelect()  # Usamos RadioSelect para una selección única
    )

    quantity = forms.IntegerField(
        required = False,
        initial = 1,
        min_value = 1
    )

    discount = forms.DecimalField( # Descuento unitario por producto (opcional para cada producto)
        required = False,
        initial = 0,
        min_value = 0
    )

    class Meta:
        model = OrderDetail
        fields = ['product', 'quantity', 'discount']

OrderDetailFormset = forms.inlineformset_factory(
    Sale,
    OrderDetail,
    form=OrderDetailForm,
    extra = 1,
)


class PaymentMethodForm(ValidationFormMixin):
    
    name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ej.: BNA, Macro, GoCuotas'
            }
        )
    )
    
    type_method = forms.ModelChoiceField(
        queryset = PaymentType.objects.exclude(name__in=['Efectivo', 'Transferencia', 'Cuenta Corriente']),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )    
    class Meta:
        model = PaymentMethod
        fields = ['name', 'type_method']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            self.validate_length(name, 3, 'Ingrese un nombre válido.')
            if PaymentMethod.objects.filter(name=name.lower()).exists():
                raise forms.ValidationError('Ya existe el Metodo de Pago.')
        return name.capitalize()


class TypePaymentMethodForm(ValidationFormMixin):

    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.exclude(name__in=['Cuenta Corriente']),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
                }
        )
    )
    description = forms.CharField(
        required = False,
        widget = forms.TextInput(
            attrs={
                'class': 'form-control'
                }
        )
    )

    class Meta:
        model = Payment
        fields = ['payment_method', 'description'] 


class SelectFacturaFrom(forms.Form):
    TYPE = [
        ('0', '---------'),
        ('A', 'Factura A'),
        ('B', 'Factura B'),
    ]

    select = forms.ChoiceField(
        choices=TYPE,
        initial=TYPE[0],
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )
