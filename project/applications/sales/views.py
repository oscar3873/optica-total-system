from django import http
from django.shortcuts import redirect, render
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

#Importaciones de la app
from applications.branches.models import Branch
from .models import *
from .forms import *



# Create your views here.
class PointOfSaleView(LoginRequiredMixin, TemplateView):
    template_name = 'sales/point_of_sale_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            branch_actualy = self.request.session.get('branch_actualy')
            branch = Branch.objects.get(id=branch_actualy)
        except Branch.DoesNotExist:
            branch = self.request.user.branch

        context['branch_selected'] = branch.name
        return context