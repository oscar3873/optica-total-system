from django import forms
from django import forms

from applications.products.models import Product
from .models import Promotion, PromotionProduct, TypePromotion


class PromotionProductForm(forms.ModelForm):
    
    type_discount = forms.ModelChoiceField(
        queryset= TypePromotion.objects.all(),
        empty_label="Elija una opción"
    )

    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        
    )

    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        
    )

    productsSelected = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required = False
    )
    
    is_active = forms.BooleanField(
        label="Activo", 
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input mb-2'}
        )
    )

    class Meta:
        model = Promotion
        fields = ['name', 'description', 'start_date', 'end_date', 'productsSelected', 'discount', 'is_active', 'user_made']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if not field_name == 'is_active':
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['required'] = ''
            
        if self.instance.pk:
            self.fields['type_discount'].initial = self.instance.type_prom
            self.fields['start_date'].initial = self.instance.start_date
            self.fields['end_date'].initial = self.instance.end_date
            self.fields['productsSelected'].initial = self.instance.promotion_products.values_list('product', flat=True)