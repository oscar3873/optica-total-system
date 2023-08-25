from django import forms

from .models import Supplier

################################################################
def validate_length(field_value, min_length, error_message):
    """
    Valida longitud de una cadena.
        Para nombres, apellidos, direcciones, telefonos, etc.
        Muestra el error mandado por argumento.
    """
    if field_value and len(field_value) < min_length:
        raise forms.ValidationError(error_message)
################################################################

class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = '__all__'
        exclude = ['user_made',]

    def clean_name(self):
        name = self.cleaned_data['name']
        validate_length(name, 3, 'El nombre del proveedor debe tener al menos 3 carácteres.')
        return name