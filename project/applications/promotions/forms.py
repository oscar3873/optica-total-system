from django import forms
from django import forms

from applications.products.models import Product
from .models import Promotion, PromotionProduct, TypePromotion


class PromotionProductForm(forms.ModelForm):
    
    type_discount = forms.ModelChoiceField(
        queryset= TypePromotion.objects.all()
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
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'product-checkboxes'}),
        required = False
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
            if not field_name in ['is_active', 'productsSelected']:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['required'] = ''
            else:
                field.widget.attrs['class'] = 'form-check-input mb-2'
            
        if self.instance:
            self.fields['type_prom'].initial = self.instance.type_prom
            self.fields['start_date'].initial = self.instance.start_date
            self.fields['end_date'].initial = self.instance.end_date
        
        if self.instance.pk:  # Update
            related_products = self.instance.promotion_products.values_list('product', flat=True)
            available_products = Product.objects.filter(id__in=related_products)
            self.fields['productsSelected'].queryset = available_products
            self.fields['productsSelected'].initial = related_products
        else:  # Create
            # Cuando creas una nueva promoción, puedes configurar el queryset del campo
            # para que muestre solo los productos relacionados con la promoción.
            related_products = PromotionProduct.objects.filter(promotion=self.instance).values_list('product', flat=True)
            available_products = Product.objects.filter(id__in=related_products)
            self.fields['productsSelected'].queryset = available_products
            
        
        
    