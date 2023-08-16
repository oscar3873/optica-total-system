from django.utils.timezone import datetime
from .models import *
from django import forms

class BranchCreateForm(forms.ModelForm):
    name = forms.CharField(
        label='Nombre de la Sucursal',
        min_length=5,
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Ej.: Sucursal 1'})
    )

    address = forms.CharField(
        label='Direccion',
        min_length=10,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ej.: Av. San Martin 2345'})
    )

    open_hs = forms.TimeField(
        label='Horario de apertura',
        required=True,
        widget=forms.TimeInput(attrs={'placeholder': '9:30'})
    )

    close_hs = forms.TimeField(
        label='Horario de cierre',
        required=True,
        widget=forms.TimeInput(attrs={'placeholder': '21:30'})
    )

    class Meta:
        model= Branch
        fields = '__all__'