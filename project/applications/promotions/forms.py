from django import forms
from django import forms

from applications.products.models import Product
from .models import Promotion, TypePromotion


class PromotionProductForm(forms.ModelForm):
    
    type_discount = forms.ModelChoiceField(
        queryset= TypePromotion.objects.all()
    )

    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
        ),
    )

    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
        ),
    )

    productsSelected = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'product-checkboxes'}),
    )
    
    is_active = forms.BooleanField(
        label="Activo", 
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check mb-2'}
        )
    )

    class Meta:
        model = Promotion
        fields = ['name', 'description', 'type_prom', 'start_date', 'end_date', 'productsSelected', 'discount', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if not field_name == 'is_active':
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['required'] = ''
            else:
                field.widget.attrs['class'] = 'form-check-input'
        
        