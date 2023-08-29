from django import forms
from applications.cashregister.models import CashRegister



class CashRegisterForm(forms.ModelForm):
    
    initial_balance = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'autofocus':''
                }
            )
        )
    
    class Meta:
        model = CashRegister
        fields = ['initial_balance']