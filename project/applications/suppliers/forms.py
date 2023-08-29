from django import forms

from .models import Supplier, Product_Supplier
from applications.products.models import Product
from applications.core.mixins import ValidationFormMixin


class SupplierForm(ValidationFormMixin):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
        )

    class Meta:
        model = Supplier
        fields = '__all__'
        exclude = ['user_made',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Update
            related_products = self.instance.product_suppliers.values_list('product__id', flat=True)
            available_products = Product.objects.exclude(id__in=related_products) | Product.objects.filter(id__in=related_products)
            self.fields['products'].queryset = available_products
            self.fields['products'].initial = related_products
        else:  # Create
            all_products = Product.objects.all()
            related_products = Product_Supplier.objects.values_list('product__id', flat=True)
            available_products = all_products.exclude(id__in=related_products)
            self.fields['products'].queryset = available_products


    def clean_name(self):
        name = self.cleaned_data['name']
        self.validate_length(name, 3, 'El nombre del proveedor debe tener al menos 3 carácteres.')
        return name