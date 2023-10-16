from django import forms

from applications.core.mixins import ValidationFormMixin
from applications.products.models import Product
from .models import *

class SaleForm(ValidationFormMixin):
    total = forms.DecimalField(
        required=False,
        initial= 0
    )
    class Meta:
        model = Sale
        fields = ['total', 'customer']


class OrderDetailForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        required=False,
        queryset=Product.objects.all(),
        widget=forms.RadioSelect()  # Usamos RadioSelect para una selección única
    )

    discount = forms.DecimalField( # Descuento unitario por producto (opcional para cada producto)
        required = False,
        initial = 0,
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


class PromotionForm(forms.ModelForm):

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
        fields = ['name', 'type_discount', 'start_date', 'end_date', 'discount', 'productA', 'productB']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = ''
        self.fields['type_discount'].initial = '2x1'

PromotionFormSet = forms.formset_factory(
    PromotionForm,
    extra=1,
    )
