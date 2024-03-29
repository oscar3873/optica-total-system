from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList

from core.mixins import ValidationFormMixin
from products.models import Product
from .models import *
from employes.models import Employee
class SaleForm(forms.ModelForm):
    description = forms.CharField(
        required = False,
        widget = forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    amount = forms.DecimalField(
        required = True,
        widget = forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )

    customer = forms.ModelChoiceField(
        required=False,
        queryset = Customer.objects.all(),
        widget = forms.RadioSelect()
    )

    # payment_method = forms.ModelChoiceField(
    #     queryset=PaymentMethod.objects.all(),
    #     empty_label=None,
    #     widget=forms.Select(
    #         attrs={'class': 'form-control'}
    #     )
    # )

    discount = forms.IntegerField(
        required=False,
        initial = 0,
        widget = forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    
    surcharge = forms.IntegerField(
        required=False,
        initial = 0,
        widget = forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = Sale
        fields = ['customer', 'discount', 'commision_user', 'surcharge']

    def __init__(self, branch=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.branch = branch
        
        self.fields['commision_user'].queryset=Employee.objects.filter(user__branch=branch)
        self.fields['commision_user'].widget.attrs['class'] = 'form-control'
    
    def clean_discount(self):
        discount = self.cleaned_data['discount']
        if not discount:
            discount = 0
        elif discount and discount < 0:
            raise forms.ValidationError('El descuento debe ser positivo')
        return discount
    
    def clean_surcharge(self):
        surcharge = self.cleaned_data['surcharge']
        if not surcharge:
            surcharge = 0
        elif surcharge and surcharge < 0:
            raise forms.ValidationError('El recargo debe ser positivo')
        return surcharge


class OrderDetailForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        required=False,
        queryset=Product.objects.all(),
        widget=forms.RadioSelect()  # Usamos RadioSelect para una selección única
    )

    quantity = forms.IntegerField(
        required = False,
        initial = 1,
        min_value = 1
    )

    discount = forms.DecimalField( # Descuento unitario por producto (opcional para cada producto)
        required = False,
        initial = 0,
        min_value = 0
    )

    class Meta:
        model = OrderDetail
        fields = ['product', 'quantity', 'discount']

OrderDetailFormset = forms.inlineformset_factory(
    Sale,
    OrderDetail,
    form=OrderDetailForm,
    extra = 1,
)


class PaymentMethodForm(ValidationFormMixin):
    
    name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ej.: BNA, Macro, GoCuotas'
            }
        )
    )
    
    type_method = forms.ModelChoiceField(
        empty_label=None,
        queryset = PaymentType.objects.exclude(name__in=['Efectivo', 'Transferencia', 'Cuenta Corriente']),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )    
    class Meta:
        model = PaymentMethod
        fields = ['name', 'type_method']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            self.validate_length(name, 3, 'Ingrese un nombre válido.')
            name = name.capitalize()
        return name
    
    def clean(self):
        cleaned_data = super().clean()
        payment = PaymentMethod.objects.filter(name=cleaned_data.get("name"))
        if payment:
            if payment.filter(type_method=cleaned_data.get('type_method')).first():
                type_method=cleaned_data.get('type_method')
                raise forms.ValidationError(f'Ya existe el metodo de pago "{payment.filter(type_method=type_method).first()}".')
        return cleaned_data


class PaymentMethodUnitForm(forms.Form):
    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.all(),
        empty_label=None,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
    
    amount = forms.DecimalField(
        required = True,
        initial=0,
        widget = forms.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
        

PaymentMethodsFormset = forms.formset_factory(
    PaymentMethodUnitForm,
    extra=1,
    )



class TypePaymentMethodForm(ValidationFormMixin):

    amount = forms.DecimalField(
        required = False,
        initial=0,
        widget = forms.NumberInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Monto'
    )

    payment_method = forms.ModelChoiceField(
        empty_label=None,
        queryset=PaymentMethod.objects.exclude(name__in=['Cuenta Corriente']),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Metodo de pago'
    )
    description = forms.CharField(
        required = False,
        widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Descripcion'
    )

    class Meta:
        model = Payment
        fields = ['payment_method', 'description', 'amount'] 


class SelectFacturaFrom(forms.Form):
    TYPE = [
        ('0', '---------'),
        ('A', 'Factura A'),
        ('B', 'Factura B'),
    ]

    select = forms.ChoiceField(
        choices=TYPE,
        initial=TYPE[0],
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )
