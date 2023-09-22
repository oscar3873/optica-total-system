from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (DeleteView, UpdateView, DetailView, FormView, ListView)
from django.contrib import messages

from applications.core.mixins import CustomUserPassesTestMixin
from applications.branches.models import Branch
from applications.cashregister.utils import obtener_nombres_de_campos

from .models import *
from .forms import *
from .utils import form_in_out_insurances

########################### CREATE ####################################
class CalibrationOrderCreateView(LoginRequiredMixin, FormView):
    model = Calibration_Order
    form_class = Calibration_OrderForm
    template_name = 'clients/lab_form.html'
    success_url = reverse_lazy('clients_app:lab_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = Calibration_OrderForm()
        context['named_formsets'] = {
            'pupilar': InterpupillaryForm,
            'correction': CorrectionForm,
            'material': MaterialForm,
            'color': ColorForm,
            'cristal': CristalForm,
            'tratamiento': TratamientForm,
        }
        return context
    
    @transaction.atomic
    def form_valid(self, form):
        try:
            customer = Customer.objects.get(pk=self.kwargs.get('pk')) # pk corresponde a como se le pasa por la url.py <pk>
        except Customer.DoesNotExist:
            raise ValueError('El ID del cliente con nuestro registro')
        
        correction_form = CorrectionForm(self.request.POST)
        material_form = MaterialForm(self.request.POST)
        color_form = ColorForm(self.request.POST)
        cristal_form = CristalForm(self.request.POST)
        tratamiento_form = TratamientForm(self.request.POST)
        pupilar_form = InterpupillaryForm(self.request.POST)

        if (
            correction_form.is_valid() and
            material_form.is_valid() and 
            color_form.is_valid() and
            cristal_form.is_valid() and 
            tratamiento_form.is_valid() and 
            pupilar_form.is_valid()
            ):

            # Create the main form instance
            Calibration_Order.objects.create_lab(
                self.request.user, form, correction_form, material_form,
                color_form, cristal_form, tratamiento_form, pupilar_form,
                customer
            )

        if customer:
            return redirect('clients_app:customer_detail', pk=self.kwargs.get('pk'))
        
        return super().form_valid(form)
    

class CustomerCreateView(LoginRequiredMixin, FormView):
    form_class = CustomerForm
    template_name = 'clients/customer_form.html'
    success_url = reverse_lazy('clients_app:customer_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['h_insurance'] = HealthInsuranceForm
        return context

    @transaction.atomic
    def form_valid(self, form):
        if form.is_valid():
            user = self.request.user
            
            customer = form.save(commit=False)
            customer.user_made = self.request.user

            if user.is_staff:
                branch_actualy = self.request.session.get('branch_actualy')
                branch_actualy = Branch.objects.get(id=branch_actualy)
                customer.branch = branch_actualy
            else:
                customer.branch = self.request.user.branch
            customer.save()

            for insurance in form.cleaned_data['h_insurance']:
                Customer_HealthInsurance.objects.create(
                    h_insurance = insurance,
                    customer = customer,
                    user_made=user
                )
        return super().form_valid(form)


class HealthInsuranceCreateView(LoginRequiredMixin, FormView):
    form_class = HealthInsuranceForm
    template_name = 'clients/insurance_form.html'
    success_url = reverse_lazy('clients_app:insurance_view')

    def form_valid(self, form):
        insurance = form.save(commit=False)
        insurance.user_made = self.request.user
        insurance.save()
        
        try:
            customer = Customer.objects.get(pk=self.kwargs.get('pk')) # pk corresponde a como se le pasa por la url.py <pk>
            Customer_HealthInsurance.objects.create(h_insurance=insurance, customer=customer)

            return redirect('clients_app:customer_detail', pk=customer.pk)
        except Customer.DoesNotExist:
            if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest': # Para saber si es una peticion AJAX
                new_insurance_data = {
                    'id': insurance.id,
                    'name': insurance.name
                }
                # Si es una solicitud AJAX, devuelve una respuesta JSON
                return JsonResponse({'status': 'success', 'new_insurance': new_insurance_data})
            else:
                # Si no es una solicitud AJAX, llama al método form_valid del padre para el comportamiento predeterminado
                return super().form_valid(form)


########################### UPDATE  #########################

class CalibrationOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Calibration_Order
    form_class = Calibration_OrderForm  # Actualizar al formulario principal si es necesario
    template_name = 'clients/lab_form.html'
    success_url = reverse_lazy('clients_app:lab_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['named_formsets'] = {
            'correction': CorrectionForm(instance=self.object.correction),
            'material': MaterialForm(instance=self.object.material),
            'color': ColorForm(instance=self.object.color),
            'cristal': CristalForm(instance=self.object.type_cristal),
            'tratamiento': TratamientForm(instance=self.object.tratamient),
            'pupilar': InterpupillaryForm(instance=self.object.interpupillary),
        }
        return context
    
    def form_valid(self, form):
        try:
            customer = Customer.objects.get(pk=self.kwargs.get('pk_c'))
        except Customer.DoesNotExist:
            raise ValueError('El ID del cliente con nuestro registro')
        
        named_formsets = self.get_context_data()['named_formsets']

        if form.is_valid():
            calibration_order = form.save(commit=False)
            for prefix, formset in named_formsets.items():
                instance = formset.instance
                new_formset = formset.__class__(self.request.POST, instance=instance)
                if new_formset.is_valid():
                    new_formset.save()
            calibration_order.save()

        if customer:
            return redirect('clients_app:customer_detail', pk=customer.pk)

        return super().form_valid(form)
    
    
class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'clients/customer_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['h_insurance'] = HealthInsuranceForm
        return context

    def form_valid(self, form):
        customer = form.instance
        customer.user_made = self.request.user
        customer.save()

        form_in_out_insurances(form, customer, self.request.user)
        
        return redirect('clients_app:customer_detail', pk=self.get_object().pk)
    
    
class HealthInsuranceUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = HealthInsurance
    form_class = HealthInsuranceForm
    template_name = 'clients/hinsurance_update.html'
    success_url = reverse_lazy('clients_app:insurance_view')
    
    def form_valid(self, form):
        insurance = form.save(commit=False)
        insurance.user_made = self.request.user
        return super().form_valid(form)

########################## DETAIL #################################


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'clients/customer_detail.html'
    context_object_name = 'customer'

    def get(self, request, *args, **kwargs):
        user = request.user
        branch = user.branch

        # Obtener el objeto Product actual utilizando self.get_object()
        object = self.get_object()

        if not user.is_staff and not object.branch == branch: 
            # El usuario no tiene permiso para ver este producto
            messages.error(request, 'Lo sentimos, no puedes ver este cliente.')
            return redirect('clients_app:customer_view')  # Reemplaza 'nombre_de_tu_vista_product_list' por el nombre correcto de la vista de lista de productos
        
        return super().get(request, *args, **kwargs)
    

    def get_context_data(self,**kwargs):
        customer = self.get_object()
        context = super().get_context_data(**kwargs)
        calibration_orders = Customer.objects.history(customer)
        context['calibration_orders'] = calibration_orders
        # AGREGAR MAS RELACIONES DEL CLIENTE: ejemplo: Ventas al cliente
        return context
    
class CalibrationOrderDetailView(LoginRequiredMixin, DetailView):
    model = Calibration_Order
    template_name = 'clients/lab_detail.html'
    context_object_name = 'laboratory_orders'


class HealthInsuranceDetailView(LoginRequiredMixin, DetailView):
    model = HealthInsurance
    template_name = 'clients/hinsuranse_detail.html'
    context_object_name = 'h_insurance'


############################## LISTING ###############################

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'clients/customer_page.html'
    context_object_name = 'customers'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_column'] = obtener_nombres_de_campos(Customer,
            "id",
            "deleted_at", 
            "created_at", 
            "updated_at",
            "phone_code",
            "branch",
            "birth_date",
            "address",
            "email"
            )
        return context

    def get_queryset(self):
        branch = self.request.user.branch
        branch_actualy = self.request.session.get('branch_actualy')
        if  self.request.user.is_staff:
            branch_actualy = Branch.objects.get(id=branch_actualy)
            # Si el usuario es administrador y hay una sucursal seleccionada en la sesión,
            return Customer.objects.filter(branch=branch_actualy, deleted_at=None)
        
        # En otros casos, filtra por la sucursal del usuario
        return Customer.objects.filter(branch=branch, deleted_at=None)


class CalibrationOrderListView(LoginRequiredMixin, ListView):
    model = Calibration_Order
    template_name = 'clients/lab_page.html'
    context_object_name = 'laboratory_orders'
    paginate_by = 8


class HealthInsuranceListView(LoginRequiredMixin, ListView):
    model = HealthInsurance
    template_name = 'clients/hinsuranse_page.html'
    context_object_name = 'h_insurances'
    paginate_by = 8


########################### DELETE ####################################

class CalibrationOrderDeleteView(CustomUserPassesTestMixin, DeleteView):
    model = Calibration_Order
    template_name = 'clients/lab_delete.html'
    context_object_name = 'laboratory'
    success_url = reverse_lazy('clients_app:lab_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            customer = Customer.objects.get(pk=self.kwargs.get('pk_c'))
            context['customer'] = customer
            return context
        except Customer.DoesNotExist:
            return context

    def get_success_url(self):
        if 'pk_c' in self.kwargs: # pk de customer pasado por url
            customer_pk = self.kwargs.get('pk_c')
            return reverse_lazy('clients_app:customer_detail', kwargs={'pk': customer_pk}) # en caso de tener pk de customer, entonces entre al delete por la vista de un cliente especifico
        return super().get_success_url() # Si entre al delete desde la lista general de pedidos de lab
        

class CustomerDeleteView(CustomUserPassesTestMixin, DeleteView):
    model = Customer
    template_name = 'clients/customer_delete.html'
    success_url = reverse_lazy('clients_app:customer_view')

    def delete(self, request, *args, **kwargs):
        customer = self.get_object()
        intermedia = Customer_HealthInsurance.objects.filter(customer=customer)
        for filas in intermedia:
            filas.delete()
        return super().delete(request, *args, **kwargs)
    

class HealthInsuranceDeleteView(CustomUserPassesTestMixin, DeleteView):
    model = HealthInsurance
    template_name = 'clients/hinsurance_delete.html'
    success_url = reverse_lazy('clients_app:insurance_view')
    
    def delete(self, request, *args, **kwargs):
        h_insurance = self.get_object()
        intermedia = Customer_HealthInsurance.objects.filter(h_insurance=h_insurance)
        for filas in intermedia:
            filas.delete()
        return super().delete(request, *args, **kwargs)