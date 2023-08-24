from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (FormView, DetailView, UpdateView, View)

from .forms import SaleForm

# Create your views here.
class SaleCreateView(LoginRequiredMixin, FormView):
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.cleaned_data['user_made'] = self.request.user
        return super().form_valid(form)