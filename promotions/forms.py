from django import forms
from django import forms

from products.models import Product
from core.mixins import ValidationFormMixin
from .models import Promotion, PromotionProduct, TypePromotion


class PromotionProductForm(ValidationFormMixin):
    
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

    def clean_name(self):
        name = self.cleaned_data['name']
        name_formated = name.title()
        self.validate_length(name_formated, 3, 'El nombre debe tener al menos 3 caracteres.')
        return name_formated
    
    def clean_discount(self):
        discount = self.cleaned_data['discount']
        if discount and discount < 0:
            raise forms.ValidationError('El valor del Descuento debe ser un numero positivo.')
        return discount
    
    def clean_description(self):
        description = self.cleaned_data['description']
        description_formated = description.title()
        return description_formated