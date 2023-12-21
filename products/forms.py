from typing import Any
from django import forms

from .models import *

from core.mixins import ValidationFormMixin
from django.core.validators import RegexValidator
from decimal import Decimal

class CategoryForm(ValidationFormMixin):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Lentes de sol'
                }
        )
    )
    class Meta:
        model = Category
        #necesario para el front
        fields = ('name',)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        name_formated = name.title()
        try:
            Category.objects.get(name=name_formated)
            raise forms.ValidationError("Ya existe una categoria con ese nombre.")
        except Category.DoesNotExist:
            pass
        self.validate_length(name_formated, 3, 'La categoria debe tener al menos 3 caracteres.')
        return name_formated


class BrandForm(ValidationFormMixin):
    name = forms.CharField(max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Rusty'
                }
        )
    )
    class Meta:
        model = Brand
        #necesario para el front 
        fields = ('name',)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        name_formated = name.title()
        try:
            Brand.objects.get(name=name_formated)
            raise forms.ValidationError("Ya existe una marca con ese nombre.")
        except Brand.DoesNotExist:
            pass
        self.validate_length(name_formated, 3, 'La categoria debe tener al menos 3 caracteres.')
        return name_formated


class ProductForm(ValidationFormMixin):

    name = forms.CharField(
        max_length=100,
        label='Nombre del producto',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto',
                }
        )
    )
    barcode = forms.IntegerField(
        required=False,
        label='Codigo de barra',
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Codigo de barra',
                'class': 'form-control',
                'placeholder' : 'Ej: 7908132209861'
                }
        ),
        error_messages={
            'min_value': 'El stock no puede ser negativo.',
        },
        validators=[
            RegexValidator(
                regex=r'^\d+$',  # Expresión regular para validar solo dígitos
                message='Ingrese solo dígitos (números).'
            )
        ]
    )
    cost_price = forms.DecimalField(
        label='Precio de costo',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Ej: 123.32',
                'class': 'form-control',
                'placeholder' : '0.00'
                }
        )
    )
    sale_price = forms.DecimalField(
        required=False,
        label='Precio de venta',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Ej: 123.32',
                'class': 'form-control',
                'placeholder' : '0.00'
                }
        )
    )
    stock = forms.IntegerField(
        label='Stock',
        max_value=9999999,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Stock',
                'type': 'number',
                #'min': 1, puede tener stock cero?
                'class': 'form-control',
                'placeholder' : 'Ej: 23'
                }
        ),
        error_messages={
            'min_value': 'El stock no puede ser negativo.',
        }
    )
    description = forms.CharField(
        max_length=100,
        label='Descripción',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Descripcion del producto',
                'type': 'text',
                'pattern': '.{3,}',  # Mínimo 3 caracteres
                'class': 'form-control',
                'placeholder' : 'Ej: marco de una sola pieza'
                }
        )
    )
    category = forms.ModelChoiceField(
        label='Categoría',
        queryset=Category.objects.all(),
        empty_label='Elija una categoria...',
        widget=forms.Select(
            attrs={
                'placeholder': 'Categoría',
                'class': 'form-control',
                'placeholder' : 'Seleccione una categoria o agregue una nueva'
                }
        )
    )
    brand = forms.ModelChoiceField(
        label='Marca',
        queryset=Brand.objects.all(),
        empty_label='Elija una marca...',
        widget=forms.Select(
            attrs={
                'placeholder': 'Marca',
                'class': 'form-control',
                }
        )
    )
    features = forms.ModelMultipleChoiceField(
        queryset=Feature.objects.all().order_by('type'),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class':'form-check-input',
                }
        ),
        required=False,
    )


    class Meta:
        model = Product
        #necesario para el front 
        fields = ('name', 'barcode', 'cost_price', 'sale_price', 'description', 'stock', 'category', 'brand')

    def __init__(self, branch=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.branch = branch
        
        if self.instance.pk:
            related_features = self.instance.product_feature.values_list('feature__id', flat=True)
            self.fields['features'].initial = related_features
    
    def clean_barcode(self):
        barcode = self.cleaned_data['barcode']
        try:
            if barcode and len(str(barcode)) > 3:
                Product.objects.get(barcode=barcode, branch=self.branch)
                raise forms.ValidationError('El codigo ingresado ya existe en la surcursal.')
        except Product.DoesNotExist:
            pass
        return barcode

    def clean_sale_price(self):
        price = self.cleaned_data.get('sale_price')
        if price and price < Decimal('0.00'):
            raise forms.ValidationError('El precio no puede ser un número negativo.')
        return price
    
    def clean_cost_price(self):
        price = self.cleaned_data.get('cost_price')
        if price and price < Decimal('0.00'):
            raise forms.ValidationError('El precio no puede ser un número negativo.')
        return price

    def clean_name(self):
        name = self.cleaned_data['name']
        name_formated = name.capitalize()
        self.validate_length(name_formated, 3, 'La categoria debe tener al menos 3 caracteres.')
        return name_formated

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock and stock < 0:
            raise forms.ValidationError('El valor de Stock debe ser un numero positivo.')
        return stock


class FeatureForm(ValidationFormMixin):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            # attrs={'class':'form-control'}
        ),
        required=False,
    )
    value = forms.CharField(
        max_length=100,
        widget = forms.TextInput(
            attrs={'class':'form-control',
                   }
        ),
    )
    type  = forms.ModelChoiceField(
        label='Tipos de Caracteristicas',
        queryset=Feature_type.objects.all(),
        empty_label='Elija el tipo de caracteristica',
        widget=forms.Select(
            attrs={
                'class':'form-control'
            })
    )

    class Meta:
        model = Feature
        fields = ('value','type')

    def clean_value(self):
        value = self.cleaned_data['value']
        value_formated = value
        try:
            Feature.objects.get(value=value_formated)
            raise forms.ValidationError("Ya existe una categoria con ese nombre.")
        except Feature.DoesNotExist:
            pass
        self.validate_length(value, 3, 'La categoria debe tener al menos 3 caracteres.')
        return value.title()


class FeatureTypeForm(ValidationFormMixin):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            })
    )
    class Meta:
        model = Feature_type
        fields = ('name',)

    def clean_name(self):
        name = self.cleaned_data['name']
        self.validate_length(name, 2, 'El nombre del tipo de característica debe tener al menos 3 caracteres.')
        return name.title()



class FeatureForm_toWizard(ValidationFormMixin):
    type = forms.CharField(
        max_length=20,
        label="Tipo de caracteristica",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Color'
                }
        )
    )
    value = forms.CharField(
        max_length=20,
        label="Valor",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Rojo'
                }
        )
    )
    class Meta:
        model = Feature
        fields = ('value',)

    def clean_type(self):
        type = self.cleaned_data['type']
        self.validate_length(type, 2, 'El tipo debe tener almenos 3 caracteres.')
        return type.title()
    
    def clean_value(self):
        value = self.cleaned_data['value']
        return value.title()


FeatureFormSet = forms.inlineformset_factory(
    Product, 
    Product_feature,
    form=FeatureForm_toWizard,
    extra=0,
    can_delete=False
    )

class UpdatePriceForm(forms.Form):
    percentage = forms.DecimalField(
        label='Porcentaje de Aumento',
        max_value=100,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    brand = forms.ModelMultipleChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    # def clean_percentage(self):
    #     percentage = self.cleaned_data['percentage']
    #     if percentage and percentage < 0:
    #         raise forms.ValidationError('El porcentaje debe ser positivo')
    #     return percentage
