import json
from typing import Any
from django import http
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
import json

#Importaciones de la app
from applications.branches.models import Branch
from applications.clients.forms import CustomerForm
from .models import *
from .forms import *

# Create your views here.

class PointOfSaleView(LoginRequiredMixin, FormView):
    form_class = OrderDetailFormset
    template_name = 'sales/point_of_sale_page.html'
    success_url = reverse_lazy('core_app:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            branch_actualy = self.request.session.get('branch_actualy')
            branch = Branch.objects.get(id=branch_actualy)
        except Branch.DoesNotExist:
            branch = self.request.user.branch

        context['sale_form'] = SaleForm

        context['branch_selected'] = branch.name
        context['customer_form'] = CustomerForm
        return context

    def form_valid(self, form):
        formsets = form
        # Procesa los datos del formulario aquí
        for formset in formsets:
            if formset.is_valid():
                print('\n\n\n',formset.cleaned_data)
            else:
                print('\n\n\n',formset.errors) 
        
        messages.success(self.request, "Se ha generado la venta con éxito!")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form: Any) -> HttpResponse:
        messages.error(self.request, "Error. Verifique los datos.")
        return super().form_invalid(form)
