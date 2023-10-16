from django import forms

from applications.products.models import Product
from .models import Promotion


class PromotionForm(forms.ModelForm):
    PROMOTION = [
        ('A', '2x1'),
        ('B', '-50% 2da unidad'),
    ]

    type_discount = forms.ChoiceField(
        choices = PROMOTION,
        initial = PROMOTION[0]
    )

    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={ 'type': 'date'}),
    )

    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={ 'type': 'date'}),
    )

    productA = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(),
    )

    productB = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(),
    )
    class Meta:
        model = Promotion
        fields = ['name', 'start_date', 'end_date', 'discount', 'productA', 'productB']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = ''
        
PromotionFormSet = forms.formset_factory(
    PromotionForm,
    extra=1,
    )
