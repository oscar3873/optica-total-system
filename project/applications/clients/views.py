from copy import copy
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from django.views.generic import (CreateView, View, DetailView)
from django.views.generic.edit import (FormView,)

from .models import Customer
from .forms import CustomerForm
from applications.core.models import Person

# Create your views here.
class CustomerCreateView(LoginRequiredMixin, FormView):
    form_class = CustomerForm
    template_name = 'customer/new_customer.html'
    success_url = reverse('core_app:home')

    def form_valid(self, form):
        data = copy(form.cleaned_data)
        data.pop('address')
        person = Person.objects.create_person_dict(**data)

        Customer.objects.creat_customer(
            person,
            form.cleaned_data['address'],
        )
        
        return super().form_valid(form)
    

# class CustomerDetailView(LoginRequiredMixin, DetailView):
