from django.utils.timezone import datetime
from .models import *
from django import forms

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
        if name and len(name) < 3:
            raise forms.ValidationError('El nombre debe contener por lo menos 4 carácteres.')
        return name
    
    def clean_address(self):
        address = self.cleaned_data['address']
        if address and len(address) < 3:
            raise forms.ValidationError('Ingrese una dirección válida.')
        return address
    