from django import forms

from .models import *

from applications.core.mixins import ValidationFormMixin

class CategoryForm(ValidationFormMixin):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['user_made','deleted_at']
    
    def clean_name(self):
        name = self.cleaned_data['name']
        self.validate_length(name, 3, 'La categoria debe tener al menos 3 caracteres.')
        return name


class BrandForm(ValidationFormMixin):
    class Meta:
        model = Brand
        fields = '__all__'
        exclude = ['user_made','deleted_at']

    def clean_name(self):
        name = self.cleaned_data['name']
        self.validate_length(name, 3, 'El nombre de la marca debe tener al menos 3 caracteres.')
        return name


class ProductForm(ValidationFormMixin):
    features = forms.ModelMultipleChoiceField(
        queryset=Feature.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['user_made','deleted_at']

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
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = Feature
        fields = [ 'type', 'value',]

class FeatureTypeForm(ValidationFormMixin):
    class Meta:
        model = Feature_type
        fields = ['name']

        def clean_name(self):
            name = self.cleaned_data['name']
            self.validate_length(name, 2, 'El nombre del tipo de característica debe tener al menos 3 caracteres.')
            return name




class FeatureForm_to_formset(ValidationFormMixin):
    type = forms.CharField(
        max_length=20,
        label="Tipo de caracteristica",
        required=False
    )
    value = forms.CharField(
        max_length=20,
        label="Valor",
        required=False
    )
    class Meta:
        model = Feature
        fields = [ 'type', 'value',]


FeatureFormSet = forms.inlineformset_factory(
    Product, 
    Product_feature,
    form=FeatureForm_to_formset,
    extra=1,
    can_delete=False
    )
