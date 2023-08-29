from django.urls import reverse_lazy
from django.views.generic import (UpdateView, DeleteView, ListView, DetailView, FormView)

from applications.core.mixins import CustomUserPassesTestMixin
from .forms import SupplierForm
from .models import Supplier

# Create your views here.
class SupplierCreateView(CustomUserPassesTestMixin, FormView):
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        supplier_data = {
            'user_made': self.request.user,
            'name': form.cleaned_data['name'],
            'email': form.cleaned_data['email'],
            'phone_number': form.cleaned_data['phone_number'],
        }
        Supplier.objects.create(**supplier_data)
        return super().form_valid(form)


class SupplierUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('core_app:home')


class SuppliersListView(CustomUserPassesTestMixin, ListView):
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
    
