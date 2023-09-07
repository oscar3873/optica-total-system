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
                }
        )
    )
    barcode = forms.IntegerField(
        label='Codigo de barra',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                }
        )
    )
    price = forms.IntegerField(
        label='Precio',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                }
        )
    )
    stock = forms.IntegerField(
        label='Stock',
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                }
        )
    )
    description = forms.CharField(
        max_length=100,
        label='Descripción',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                }
        )
    )
    category = forms.ModelChoiceField(
        label='Categoría',
        queryset=Category.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                }
        )
    )
    brand = forms.ModelChoiceField(
        label='Marca',
        queryset=Brand.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                }
        )
    )
    features = forms.ModelMultipleChoiceField(
        queryset=Feature.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            # attrs={'class':'form-control'}
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
            self.fields['features'].queryset = Feature.objects.all()
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
        label='Categoría',
        queryset=Feature_type.objects.all(),
    )

    class Meta:
        model = Feature
        fields = ('value','type')
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class':'form-control'}) 


class FeatureTypeForm(ValidationFormMixin):
    name = forms.CharField(max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                }
        )
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
        fields = ('type', 'value',)


FeatureFormSet = forms.inlineformset_factory(
    Product, 
    Product_feature,
    form=FeatureForm_to_formset,
    extra=0,
    can_delete=False
    )
