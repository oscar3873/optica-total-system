from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views.generic import (CreateView, View, DetailView)
from django.views.generic.edit import (FormView,)

from .models import HealthInsurance
from .models import Customer
from .forms import CustomerForm, HealthInsuranceForm

# Create your views here.
class CustomerCreateView(LoginRequiredMixin, FormView):
    form_class = CustomerForm
    template_name = 'clients/new_customer.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        customer_data = form.cleaned_data
        Customer.objects.create_customer(**customer_data)
        return super().form_valid(form)


class HealthInsuranceCreateView(LoginRequiredMixin, CreateView):
    form_class = HealthInsuranceForm
    template_name = 'clients/new_health_insurance.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        HealthInsurance.objects.create(
            name = form.cleaned_data['name'],
            cuit = form.cleaned_data['cuit']
        )
        return super().form_valid(form)