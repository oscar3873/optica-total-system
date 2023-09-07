from django.shortcuts import render
from django.views.generic import *
from applications.cashregister.forms import CashRegisterForm, MovementForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse

#Importaciones de la app
from applications.branches.models import Branch
from applications.cashregister.models import CashRegister, CashRegisterDetail, TypeMethodePayment, Currency, Movement
from applications.cashregister.forms import CloseCashRegisterForm, CashRegisterDetailForm, CashRegisterDetailFormSet
from applications.cashregister.utils import obtener_nombres_de_campos


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
        print("----------------Success form creation cashregister----------------")
        print(form.data)
        
        #Esto hay que cambiarlo la sucursal la debe sacar de self.request.user.branch
        branch = self.request.user.branch
        
        # Verifica si ya hay una caja registradora activa para la sucursal actual
        if CashRegister.objects.filter(branch=branch, is_close=False).exists():
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
        print("----------------Error form creation cashregister----------------")
        print(form.data)
        messages.error(self.request, 'Existe un error en el formulario o Ya existe una caja abierta. Consulte al administrador del sistema por este mensaje')
        return super().form_invalid(form)

class CashRegisterView(TemplateView):
    template_name = 'cashregister/cashregister_page.html'
    model = CashRegister
    form_class = CloseCashRegisterForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí se recupera la caja de la sucursal correspondiente al usuario logueado
        branch = self.request.user.branch
        try:
            cashregister = CashRegister.objects.get(branch=branch, is_close=False)
        except CashRegister.DoesNotExist:
            cashregister = None
        context['cashregister'] = cashregister
        return context
    
    def post(self, request, *args, **kwargs):
        print("----------------Success post close cashregister----------------")
        print(request.POST)
        
        form = self.form_class(request.POST)
        if form.is_valid():
            # Aquí se recupera la caja de la sucursal correspondiente al usuario logueado
            branch = request.user.branch
            try:
                cash_register = CashRegister.objects.get(branch=branch, is_close=False)
            except CashRegister.DoesNotExist:
                messages.error(request, 'No hay una caja registradora activa para esta sucursal')
                return self.render_to_response(self.get_context_data(form=form))
            cash_register.close_cash_register(form.cleaned_data['final_balance'])
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


class CashRegisterClosedView(View):
    template_name = 'cashregister/cashregister_closed_page.html'
    
    def get(self, request, *args, **kwargs):
        initial_data = [{'type_method': method} for method in TypeMethodePayment.objects.all()]
        formset = CashRegisterDetailFormSet(initial=initial_data)
        
        return render(request, self.template_name, {'formset': formset})
    
    def post(self, request, *args, **kwargs):
        formset = CashRegisterDetailFormSet(request.POST)
        
        #Falta implementar la logica completa para el arqueo y el cierre en los managers.py
        
        if formset.is_valid():
            print("----------------Success formset create cashregister----------------")
            cashregister = CashRegister.objects.get(is_close=False)
            for form in formset:
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.user_made = request.user
                    instance.cash_register = cashregister
                    instance.save()
            # IMPORTANTE CON ESTO SE CIERRA LA CAJA
            cashregister.is_close = True
            cashregister.save()
            
        else:
            print("----------------Error formset create cashregister----------------")
            messages.error(request, 'Existe un error en el formulario. Consulte al administrador del sistema por este mensaje')
        return render(request, self.template_name, {'formset': formset})


class MovementsView(TemplateView):
    template_name = 'cashregister/movements_page.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí se recupera la caja de la sucursal correspondiente al usuario logueado
        branch = self.request.user.branch
        try:
            cashregister = CashRegister.objects.get(branch=branch, is_close=False)
        except CashRegister.DoesNotExist:
            cashregister = None
        
        movements = Movement.objects.filter(cash_register=cashregister)    
        
        context['movements'] = movements
        context['table_column'] = obtener_nombres_de_campos(Movement, "description", "currency", "transaction_id",  "id", "deleted_at", "created_at", "updated_at", "withdrawal_reason")
        
        return context

class MovementsCreateView(FormView):
    template_name = 'cashregister/movements_create_page.html'
    model = Movement
    form_class = MovementForm
    success_url = reverse_lazy('cashregister_app:movements_view')
    
    def form_valid(self, form):
        print("----------------Success form creation movements----------------")
        print(form.data)
        
        branch = self.request.user.branch
        cash_register = CashRegister.objects.get(branch=branch, is_close=False)
        
        form.instance.date_movement = timezone.now()
        form.instance.cash_register = cash_register
        form.instance.currency = cash_register.currency
        form.instance.user_made = self.request.user
        form.save()
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("----------------Error form creation movements----------------")
        print(form.data)
        return super().form_invalid(form)


class MovementsDeleteView(DeleteView):
    template_name = 'cashregister/movements_delete_page.html'
    model = Movement
    success_url = reverse_lazy('cashregister_app:movements_view')
    
    def delete(self, request, *args, **kwargs):
        print("----------------Success delete movements----------------")
        print(request.POST)
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Eliminar movimiento"
        context['form_description'] = "¿Está seguro que desea eliminar este movimiento?"
        return context
    
    def post(self, request, *args, **kwargs):
        print("----------------Success post delete movements----------------")
        print(request.POST)
        return super().post(request, *args, **kwargs)
    

class MovementsUpdateView(UpdateView):
    template_name = 'cashregister/movements_update_page.html'
    model = Movement
    form_class = MovementForm
    
    def form_valid(self, form):
        print("----------------Success form update movements----------------")
        print(form.data)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("----------------Error form update movements----------------")
        print(form.data)
        return super().form_invalid(form)


class MovementsClosedView(TemplateView):
    template_name = 'cashregister/cashregister_closed_page.html'


#------- VISTAS BASADAS EN FUNCIONES PARA PETICIONES AJAX -------#

