from django import forms
from django.forms import formset_factory
from cashregister.models import CashRegister, CashRegisterDetail, Movement, Currency
from sales.models import PaymentType



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
        empty_label=None,
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
    
    observations = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'class': 'form-control',
                'rows': '5',
                'placeholder': 'Ej. Falto plata de ...'
            }
        )
    )
    
    class Meta:
        model = CashRegister
        fields = ['observations']


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
    
    amount = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '0.00'
            }
        )
    )
    TYPE_OPERATION = [
        ('Ingreso', 'Ingreso'),
        ('Egreso', 'Egreso')
    ]

    type_operation = forms.ChoiceField(
        initial=TYPE_OPERATION[0],
        choices=TYPE_OPERATION,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione una opción'
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '5',
                'placeholder': 'Se retiró para la compra de ...'
            }
        )
    )

    payment_method = forms.ModelChoiceField(
        queryset=PaymentType.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione una opción'
            }
        )
    )
    class Meta:
        model = Movement
        fields = ['amount', 'type_operation', 'description', 'payment_method']


CashRegisterDetailFormSet = formset_factory(CashRegisterDetailForm, extra=0)