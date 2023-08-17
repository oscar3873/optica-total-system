from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views.generic import (CreateView, View, DetailView)
from django.views.generic.edit import (FormView,)

from .forms import CustomerForm
from .services import set_person_to_customer

# Create your views here.
class CustomerCreateView(LoginRequiredMixin, FormView):
    form_class = CustomerForm
    template_name = 'clients/new_customer.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        set_person_to_customer(form)
        
        return super().form_valid(form)
    

# class CustomerDetailView(LoginRequiredMixin, DetailView):
