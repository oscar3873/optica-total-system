from django import forms

from .models import Category, Brand, Product, Feature, Feature_type

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
    features = forms.ModelMultipleChoiceField(
        queryset=Feature.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={'class':'form-control'}
        ),
        required=False,
    )

    name = forms.CharField(max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                }
        )
    )

    class Meta:
        model = Product
        #necesario para el front 
        fields = ('name',)

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
            attrs={'class':'form-control'}
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
        queryset=Feature_type.objects.all(),
    )

    """ type = forms.ModelChoiceField(queryset= Feature_type.objects.all()) """

    class Meta:
        model = Feature
        fields = ['value','type','products']
    
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
        fields = ['name']

        def clean_name(self):
            name = self.cleaned_data['name']
            self.validate_length(name, 2, 'El nombre del tipo de característica debe tener al menos 3 caracteres.')
            return name