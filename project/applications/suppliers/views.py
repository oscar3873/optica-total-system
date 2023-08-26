from django.urls import reverse_lazy
from django.views.generic import (View, CreateView, DeleteView, ListView, DetailView, FormView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SupplierForm
from .models import Supplier

# Create your views here.
class SupplierCreateView(LoginRequiredMixin, CreateView):
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('core_app:home')


class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('core_app:home')


class SuppliersListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'suppliers/supplier_list.html'
    context_object_name = 'suppliers'
    

class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'suppliers/supplier_detail.html'
    context_object_name = 'supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_products_suppliers'] = Supplier.objects.get_all_products(self.get_object())
        return context
    