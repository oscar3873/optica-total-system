from .models import *
from django import forms

from applications.core.mixins import ValidationFormMixin


class BranchForm(ValidationFormMixin):
    """
    Formulario para ingresar una nueva sucursal (?).
        fields: [name, adress, open_hs, close_hs]
    """
    name = forms.CharField( #esto
        label='Nombre',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    address = forms.CharField( #esto
        label='Dirección',
        widget=forms.TextInput(
            attrs={'class': 'form-control'
                   }
        )
    )

    open_hs = forms.TimeField(
        label='Horario de Apetura',
        widget=forms.TimeInput(
            attrs={'class': 'form-control',
                   'type': 'time'
                   },
            format='%H:%M'
        )
    )

    close_hs = forms.TimeField(
        label='Horario de Cierre',
        widget=forms.TimeInput(
            attrs={'class': 'form-control',
                   'type': 'time'
                   },
            format='%H:%M'
        )
    )

    class Meta:
        model= Branch
        fields = '__all__'
        exclude = ['user_made',]

    def clean_name(self):
        name = self.cleaned_data['name']
        self.validate_length(name, 3, "Ingrese una dirección válida.") #ingrese un nombre valido
        return name
    
    def clean_address(self):
        address = self.cleaned_data['address']
        self.validate_length(address, 5, "Ingrese una dirección válida.")
        return address
    