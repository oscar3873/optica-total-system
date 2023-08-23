from django import forms

from .models import *

class SaleForm(forms.ModelForm):

    class Meta:
        model = Sale
        fields = '__all__'
        exclude = ['refund_date']
