from django import forms

from .models import Supplier
from applications.core.forms import validate_length


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = '__all__'
        exclude = ['user_made',]

    def clean_name(self):
        name = self.cleaned_data['name']
        validate_length(name, 3, 'El nombre del proveedor debe tener al menos 3 carácteres.')
        return name