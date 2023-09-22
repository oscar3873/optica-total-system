import json
from typing import Any
from django import http
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
import json

#Importaciones de la app
from applications.branches.models import Branch
from .models import *
from .forms import *


# Create your views here.

class PointOfSaleView(LoginRequiredMixin, FormView):
    form_class = OrderDetailForm
    template_name = 'sales/point_of_sale_page.html'
    success_url = reverse_lazy('core_app:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            branch_actualy = self.request.session.get('branch_actualy')
            branch = Branch.objects.get(id=branch_actualy)
        except Branch.DoesNotExist:
            branch = self.request.user.branch

        context['branch_selected'] = branch.name
        return context

    def form_valid(self, form):
        # Procesa los datos del formulario aquí
        selected_products = form.cleaned_data['products']
        print('\n\n\n\n', form.cleaned_data)        
        if selected_products:
            for product in selected_products:
                cantidad_field_name = f'cantidad-{product.id}'
                cantidad = form.cleaned_data[cantidad_field_name]
                
        else:
            messages.error(self.request, "Debe Seleccionar un producto al menos para continuar con la venta.")
            return super().form_invalid(form)
        
        messages.success(self.request, "Se ha generado la venta con éxito!")
        return HttpResponseRedirect(self.success_url)
