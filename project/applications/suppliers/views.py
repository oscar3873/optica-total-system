from django.urls import reverse_lazy
from django.views.generic import (View, FormView, DeleteView, ListView, DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SupplierForm
from .models import Supplier

# Create your views here.
class SupplierCreateView(LoginRequiredMixin, FormView):
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

class SuppliersListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'suppliers/supplier_list.html'
    context_object_name = 'suppliers'
    
    def get_queryset(self):
        return Supplier.objects.all()
    

class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'suppliers/supplier_detail.html'
    context_object_name = 'supplier'

    def get_queryset(self):
        return Supplier.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_products_suppliers'] = Supplier.objects.get_all_products(self.get_object())
        return context