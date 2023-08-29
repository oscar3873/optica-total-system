from django.shortcuts import render
from django.views.generic import *
from applications.cashregister.forms import CashRegisterForm
from django.urls import reverse_lazy
from django.contrib import messages

#Importaciones temporales
from applications.branches.models import Branch
from applications.cashregister.models import Currency
from applications.cashregister.models import CashRegister


# Create your views here.
class CashRegisterCreateView(FormView):
    template_name = 'cashregister/cashregister_create_page.html'
    form_class = CashRegisterForm
    success_url = reverse_lazy('cashregister_app:cashregister_view')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cashregister'] = CashRegister.objects.all()
        return context
    
    def form_valid(self, form):
        print("----------------Success form----------------")
        print(form.data)
        
        #Esto hay que cambiarlo la sucursal la debe sacar de self.request.user.branch
        branch = Branch.objects.all()[0]
        
        # Verifica si ya hay una caja registradora activa para la sucursal actual
        if CashRegister.objects.filter(branch=branch, is_active=True).exists():
            return super().form_invalid(form)
        
        initial_balance = form.cleaned_data['initial_balance']
        user_made = self.request.user
        currency = Currency.objects.get(code='ARS')  # o cualquier otra lógica para obtener la moneda

        try:
            cash_register = CashRegister.objects.create_cash_register(initial_balance, branch, user_made, currency)
        except Exception as e:
            # manejar error
            print(e)
            return super().form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        print("----------------Error form----------------")
        print(form.data)
        messages.error(self.request, 'Existe un error en el formulario o Ya existe una caja abierta. Consulte al administrador del sistema por este mensaje')
        return super().form_invalid(form)
    

class CashRegisterView(TemplateView):
    template_name = 'cashregister/cashregister_page.html'
    model = CashRegister
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Aqui se recupera la caja de la sucursal correspondiente al usuario logueado
        context['cashregister'] = CashRegister.objects.first()
        return context
    

class MovementsView(TemplateView):
    template_name = 'cashregister/movements_page.html'


class MovementsClosedView(TemplateView):
    template_name = 'cashregister/cashregister_closed_page.html'
    