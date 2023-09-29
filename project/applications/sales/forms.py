from django import forms

from applications.core.mixins import ValidationFormMixin
from applications.products.models import Product
from .models import *

class SaleForm(ValidationFormMixin):
    class Meta:
        model = Sale
        fields = ['total',]


class OrderDetailForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        required=False,
        queryset=Product.objects.all(),
        widget=forms.RadioSelect()  # Usamos RadioSelect para una selección única
    )

    class Meta:
        model = OrderDetail
        fields = ['product', 'quantity']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar un campo de cantidad para cada producto seleccionado
        self.fields['quantity'].required = False

OrderDetailFormset = forms.inlineformset_factory(
    Sale,
    OrderDetail,
    form=OrderDetailForm,
    extra = 0,
)