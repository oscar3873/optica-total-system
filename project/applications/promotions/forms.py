from django import forms
from django import forms

from applications.products.models import Product
from .models import Promotion, TypePromotion


class PromotionProductForm(forms.ModelForm):
    type_promotions = TypePromotion.objects.all().values_list('id', 'name')
    
    type_discount = forms.ChoiceField(
        choices=type_promotions,
        initial = type_promotions[0] if type_promotions else None
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

    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'product-checkboxes'}),
    )

    class Meta:
        model = Promotion
        fields = ['name', 'description', 'type_prom', 'start_date', 'end_date', 'products']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = ''