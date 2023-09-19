from typing import Any
from django import http
from django.shortcuts import redirect, render
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone

#Importaciones de la app
from applications.branches.models import Branch
from .models import *
from .forms import *



# Create your views here.
class PointOfSaleView(TemplateView):
    template_name = 'sales/point_of_sale_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context