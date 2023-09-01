from django import forms
from django.forms import formset_factory
from applications.cashregister.models import CashRegister, CashRegisterDetail



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
        

class CloseCashRegisterForm(forms.Form):
    
    final_balance = forms.DecimalField(
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
        fields = ['final_balance']

class CashRegisterDetailForm(forms.ModelForm):
    
    class Meta:
        model = CashRegisterDetail
        fields = ['type_method', 'registered_amount', 'counted_amount', 'difference']
        widgets = {
            'type_method': forms.Select(
                attrs={
                    'class': 'form-control border-0 bg-transparent', 
                }),
            'registered_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'counted_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'difference': forms.NumberInput(attrs={'class': 'form-control'}),
        }


CashRegisterDetailFormSet = formset_factory(CashRegisterDetailForm, extra=0)