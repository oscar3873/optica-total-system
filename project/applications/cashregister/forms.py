from django import forms
from django.forms import formset_factory
from applications.cashregister.models import CashRegister, CashRegisterDetail, Movement, Currency



class CurrencyForm(forms.ModelForm):
    
    class Meta:
        model = Currency
        fields = ['name', 'symbol', 'code']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ejemplo: Peso Argentino',
                    'required':''
                    }
                ),
            'symbol': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ejemplo: $',
                    'required':''
                    }
                ),
            'code': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ejemplo: ARS',
                    'required':''
                    }
                ),
            }


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
    
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione una opción'
            }
        )
    )
    
    class Meta:
        model = CashRegister
        fields = ['initial_balance', 'currency']
        

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
        fields = ['counted_amount']
        widgets = {
            'counted_amount': forms.NumberInput(
                attrs={
                    'class': 'form-control difference-input',
                    'placeholder': '0.00',
                })
        }
        

class MovementForm(forms.ModelForm):
    
    class Meta:
        model = Movement
        fields = ['amount', 'type_operation', 'description', 'payment_method']
        widgets = {
            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0.00'
                }),
            'type_operation': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Seleccione una opción'
                }),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '5',
                    'placeholder': 'Se retiro para compra de ...'
                }),
            'payment_method': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Seleccione una opción'
                })
        }
        
        

CashRegisterDetailFormSet = formset_factory(CashRegisterDetailForm, extra=0)