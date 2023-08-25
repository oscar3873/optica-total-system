from django import forms

from .models import Category, Brand, Product, Feature, Feature_type

from applications.core.forms import validate_length

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['user_made',]
    
    def clean_name(self):
        name = self.cleaned_data['name']
        validate_length(name, 3, 'La categoria debe tener al menos 3 caracteres.')
        return name


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'
        exclude = ['user_made',]

    def clean_name(self):
        name = self.cleaned_data['name']
        validate_length(name, 3, 'El nombre de la marca debe tener al menos 3 caracteres.')
        return name


class ProductForm(forms.ModelForm):
    features = forms.ModelMultipleChoiceField(
        queryset=Feature.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['user_made',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            related_features = self.instance.product_feature.values_list('feature__id', flat=True)
            self.fields['features'].queryset = Feature.objects.all()
            self.fields['features'].initial = related_features

    def clean_name(self):
        name = self.cleaned_data['name']
        validate_length(name, 3, 'El nombre del producto debe tener al menos 3 caracteres.')
        return name

class FeatureForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = Feature
        fields = '__all__'
        exclude = ['user_made',]

class FeatureTypeForm(forms.ModelForm):
    class Meta:
        model = Feature_type
        fields = '__all__'
        exclude = ['user_made',]

        def clean_name(self):
            name = self.cleaned_data['name']
            validate_length(name, 2, 'El nombre del tipo de característica debe tener al menos 3 caracteres.')
            return name