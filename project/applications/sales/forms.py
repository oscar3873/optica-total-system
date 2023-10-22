from django import forms

from applications.core.mixins import ValidationFormMixin
from applications.products.models import Product
from .models import *

class SaleForm(forms.ModelForm):
    MODEL_CHOICES = (
        ('C', 'No generar'),
        ('A', 'Factura'),
        ('B', 'Ticket comun')
    )

    has_proof = forms.ChoiceField(
        required= False,
        choices = MODEL_CHOICES,
        initial = MODEL_CHOICES[0],
        widget = forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    total = forms.DecimalField(
        required=False,
        initial= 0
    )

    customer = forms.ModelChoiceField(
        required=False,
        queryset = Customer.objects.all(),
        widget = forms.RadioSelect()
    )
    class Meta:
        model = Sale
        fields = ['total', 'customer',]


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
