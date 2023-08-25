from django.utils.timezone import datetime
from .models import *
from django import forms

from applications.core.forms import validate_length


class BranchForm(forms.ModelForm):
    open_hs = forms.TimeField(
        label='Horario de Apertura',
        widget=forms.TimeInput(
            attrs={'class': 'form-control', 'type': 'time'},
            format='%H:%M'
        )
    )

    close_hs = forms.TimeField(
        label='Horario de Cierre',
        widget=forms.TimeInput(
            attrs={'class': 'form-control', 'type': 'time'},
            format='%H:%M'
        )
    )

    class Meta:
        model= Branch
        fields = '__all__'
        exclude = ['user_made',]

    def clean_name(self):
        name = self.cleaned_data['name']
        validate_length(name, 3, "Ingrese una dirección válida.")
        return name
    
    def clean_address(self):
        address = self.cleaned_data['address']
        validate_length(address, 5, "Ingrese una dirección válida.")
        return address
    