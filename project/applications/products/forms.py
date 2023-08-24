from django import forms

from .models import Category, Brand, Product, Feature, Feature_type

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['user_made',]

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'
        exclude = ['user_made',]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['user_made',]

class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = '__all__'
        exclude = ['user_made',]

class FeatureTypeForm(forms.ModelForm):
    class Meta:
        model = Feature_type
        fields = '__all__'
        exclude = ['user_made',]