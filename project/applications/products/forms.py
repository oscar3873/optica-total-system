from django import forms

from .models import *

from applications.core.mixins import ValidationFormMixin

class CategoryForm(ValidationFormMixin):
    name = forms.CharField(max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                }
        )
    )
    class Meta:
        model = Category
        #necesario para el front 
        fields = ('name',)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        self.validate_length(name, 3, 'La categoria debe tener al menos 3 caracteres.')
        return name


class BrandForm(ValidationFormMixin):
    name = forms.CharField(max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                }
        )
    )
    class Meta:
        model = Brand
        #necesario para el front 
        fields = ('name',)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        self.validate_length(name, 3, 'El nombre de la marca debe tener al menos 3 caracteres.')
        return name


class ProductForm(ValidationFormMixin):

    name = forms.CharField(
        max_length=100,
        label='Nombre del producto',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto',
                'type': 'text',
                'pattern': '.{3,}',  # Mínimo 3 caracteres
                }
        )
    )
    barcode = forms.IntegerField(
        label='Codigo de barra',
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Codigo de barra',
                'type': 'number',
                'class': 'form-control',
                'placeholder' : 'Ej: 7908132209861'
                }
        )
    )
    price = forms.IntegerField(
        label='Precio',
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Precio',
                'type': 'number',
                'class': 'form-control',
                'placeholder' : '0.00'
                }
        )
    )
    stock = forms.IntegerField(
        label='Stock',
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Stock',
                'type': 'number',
                #'min': 1, puede tener stock cero?
                'class': 'form-control',
                'placeholder' : 'Ej: 23'
                }
        )
    )
    description = forms.CharField(
        max_length=100,
        label='Descripción',
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
        widget=forms.Select(
            attrs={
                'placeholder': 'Categoría',
                #'type': 'text',
                'class': 'form-control',
                'placeholder' : 'Seleccione una categoria o agregue una nueva'
                }
        )
    )
    brand = forms.ModelChoiceField(
        label='Marca',
        queryset=Brand.objects.all(),
        widget=forms.Select(
            attrs={
                'placeholder': 'Marca',
                #'type': 'text',
                'class': 'form-control',
                }
        )
    )
    features = forms.ModelMultipleChoiceField(
        queryset=Feature.objects.all().order_by('type'),
        widget=forms.CheckboxSelectMultiple(
            attrs={'class':'form-check-input',
                   'type' : 'checkbox'
                   }
        ),
        required=False,
    )
    class Meta:
        model = Product
        #necesario para el front 
        fields = ('name', 'barcode', 'price', 'description', 'stock', 'category', 'brand')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance.pk:
            related_features = self.instance.product_feature.values_list('feature__id', flat=True)
            self.fields['features'].initial = related_features

    def clean_name(self):
        name = self.cleaned_data['name']
        self.validate_length(name, 3, 'El nombre del producto debe tener al menos 3 caracteres.')
        return name


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
            attrs={'class':'form-control'}
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
        return name



class FeatureForm_to_formset(ValidationFormMixin):
    type = forms.CharField(
        max_length=20,
        label="Tipo de caracteristica",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
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
                }
        )
    )
    class Meta:
        model = Feature
        fields = ('value',)

    def clean_type(self):
        type = self.cleaned_data['type'].upper()
        self.validate_length(type, 2, 'El tipo debe tener almenos 3 caracteres.')
        return type
    
    def clean_value(self):
        value = self.cleaned_data['value'].upper()
        return value


FeatureFormSet = forms.inlineformset_factory(
    Product, 
    Product_feature,
    form=FeatureForm_to_formset,
    extra=0,
    can_delete=False
    )
