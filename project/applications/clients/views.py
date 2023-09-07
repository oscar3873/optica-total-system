from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, UpdateView, DetailView, FormView, ListView)

from project.applications.core.mixins import CustomUserPassesTestMixin

from .models import *
from .forms import *

########################### CREATE ####################################
class CalibrationOrderCreateView(LoginRequiredMixin, FormView):
    model = Calibration_Order
    form_class = Calibration_OrderForm
    template_name = 'clients/lab_form.html'
    success_url = reverse_lazy('core_app:home')

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
    
    def form_valid(self, form):
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
            Calibration_Order.objects.create_or_update_calibration_order(
                self.request.user, form, correction_form, material_form,
                color_form, cristal_form, tratamiento_form, pupilar_form
            )

            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class CalibrationOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Calibration_Order
    form_class = Calibration_OrderForm  # Actualizar al formulario principal si es necesario
    template_name = 'clients/lab_form.html'
    success_url = reverse_lazy('core_app:home')
    pk_url_kwarg = 'pk'  # Asegurarse de proporcionar el nombre correcto de la URL

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
        named_formsets = self.get_context_data()['named_formsets']
        
        if form.is_valid():
            # Guarda la instancia principal (Calibration_Order)
            calibration_order = form.save(commit=False)
            
            # Guarda cada formulario asociado y obtén las instancias
            for prefix, formset in named_formsets.items():
                instance = formset.instance
                new_formset = formset.__class__(self.request.POST, instance=instance)
                if new_formset.is_valid():
                    new_formset.save()
            
            calibration_order.save()  # Guarda la instancia principal
            
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    

class CustomerCreateView(LoginRequiredMixin, FormView):
    form_class = CustomerForm
    template_name = 'clients/customer_form.html'
    success_url = reverse_lazy('clients_app:customer_list')
    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.user_made = self.request.user
        customer.save()
        return super().form_valid(form)
    
class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'clients/customer_form.html'
    success_url = reverse_lazy('clients_app:customer_list')

    def form_valid(self, form):
        form.instance.user_made = self.request.user
        return super().form_valid(form)


class HealthInsuranceCreateView(LoginRequiredMixin, FormView):
    form_class = HealthInsuranceForm
    template_name = 'clients/insurance_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        insurance = form.save(commit=False)
        insurance.user_made = self.request.user
        insurance.save()
        return super().form_valid(form)
class HealthInsuranceUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = HealthInsurance
    form_class = HealthInsuranceForm
    template_name = 'clients/insurance_form.html'
    success_url = reverse_lazy('core_app:home')
    
    def form_valid(self, form):
        insurance = form.save(commit=False)
        insurance.user_made = self.request.user
        insurance.save()
        return super().form_valid(form)


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'clients/customer_detail.html'
    context_object_name = 'customer'

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'clients/client_page.html'
    context_object_name = 'customers'

########################### DELETE ####################################

class CalibrationOrderDeleteView(CustomUserPassesTestMixin, FormView):
    model = Calibration_Order
    form_class = Calibration_OrderForm
    template_name = 'clients/lab_form.html'
    success_url = reverse_lazy('core_app:home')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Realiza la eliminación suave
        return HttpResponseRedirect(self.get_success_url())

class CustomerDeleteView(CustomUserPassesTestMixin, FormView):
    model = Customer
    form_class = CustomerForm
    template_name = 'clients/customer_form.html'
    success_url = reverse_lazy('core_app:home')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Realiza la eliminación suave
        return HttpResponseRedirect(self.get_success_url())

class HealthInsuranceDeleteView(CustomUserPassesTestMixin, FormView):
    model = HealthInsurance
    form_class = HealthInsuranceForm
    template_name = 'clients/insurance_form.html'
    success_url = reverse_lazy('core_app:home')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        lista  = Customer_HealthInsurance.objects.filter(customer=self.object)
        for i in lista:
            i.delete()
        self.object.delete()  # Realiza la eliminación suave
        return HttpResponseRedirect(self.get_success_url())