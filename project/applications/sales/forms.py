from django import forms

from applications.core.mixins import ValidationFormMixin
from applications.products.models import Product
from .models import *

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


class OrderDetailForm(forms.ModelForm):
    # products = forms.ModelMultipleChoiceField(
    #     queryset=Product.objects.all(),
    #     widget=forms.CheckboxSelectMultiple(
    #         attrs={
    #                'type' : 'checkbox'
    #                }
    #     ),
    #     required=False,
    # )
    class Meta:
        model = OrderDetail
        fields = ['product', 'quantity']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar un campo de cantidad para cada producto seleccionado
        self.fields['product'].required = False
        
        # for product in self.fields['products'].queryset:
        #     self.fields[f'cantidad-{product.id}'] = forms.IntegerField(
        #         required=False,
        #         initial=0,  # Puedes establecer un valor inicial predeterminado
        #     )


OrderDetailFormset = forms.formset_factory(
    OrderDetailForm,
    extra = 0
)