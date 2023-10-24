from django import forms

from applications.core.mixins import ValidationFormMixin
from applications.products.models import Product
from applications.cashregister.models import PaymentMethod, PaymentType
from applications.cashregister.models import Payment, PaymentMethod
from .models import *

class SaleForm(forms.ModelForm):
    MODEL_CHOICES = (
        ('C', 'No generar'),
        ('A', 'Factura'),
        ('B', 'Ticket comun')
    )

    has_proof = forms.ChoiceField(
        required= False,
        choices = MODEL_CHOICES,
        initial = MODEL_CHOICES[0],
        widget = forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    customer = forms.ModelChoiceField(
        required=False,
        queryset = Customer.objects.all(),
        widget = forms.RadioSelect()
    )
    
    class Meta:
        model = Sale
        fields = ['customer',]


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

"""
class PaymentType(BaseAbstractWithUser):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    


#ESTO VA EN LA APLICACION DE SALES
class PaymentMethod(BaseAbstractWithUser):
    name = models.CharField(max_length=50)
    type_method = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + ' - ' + str(self.type_method)

"""

class PaymentMethodForm(forms.ModelForm):
    
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
        queryset=PaymentType.objects.exclude(name__in=['Efectivo', 'Transferencia']), #Tener en cuenta este "hardcodeo" para solo se tenga en cuenta Tarjeta de debito o credito, sin tener en cuenta efectivo y transferencia
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )    
    class Meta:
        model = PaymentMethod
        fields = ['name', 'type_method']
