from django import forms

from applications.core.mixins import ValidationFormMixin
from applications.products.models import Product
from .models import Sale

class SaleForm(ValidationFormMixin):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={'class':'form-check-input',
                   'type' : 'checkbox'
                   }
        ),
        required=False,
    )

    class Meta:
        model = Sale
        fields = ['total',]