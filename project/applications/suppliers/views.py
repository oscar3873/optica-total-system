from django.urls import reverse_lazy
from django.views.generic import (UpdateView, DeleteView, ListView, DetailView, FormView)

from applications.core.mixins import CustomUserPassesTestMixin
from .forms import SupplierForm
from .models import Supplier, Product_Supplier

# Create your views here.
class SupplierCreateView(CustomUserPassesTestMixin, FormView):
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        supplier = form.save(commit=False)
        supplier.user_made = self.request.user
        supplier.save()

        for product in form.cleaned_data['products']:
            Product_Supplier.objects.create(supplier=supplier, product=product, user_made = self.request.user)
        return super().form_valid(form)


class SupplierUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        form.instance.user_made = self.request.user
        supplier = form.save()

        selected_products = form.cleaned_data['products']
        existing_products = supplier.product_suppliers.all()

        # Elimina relaciones existentes que ya no están seleccionadas
        for product_suppliers in existing_products: # product_suppliers es la tabla intermedia (relacion inversa)
            if product_suppliers.product not in selected_products:
                supplier.product_suppliers.get(product=product_suppliers.product).delete()

        # Crea nuevas relaciones solo para características no existentes
        for product in selected_products:
            if product not in existing_products.values_list('product', flat=True): # Si NO existe ya un producto relacionado con el proveedor, crea la relacion
                Product_Supplier.objects.create(supplier=supplier, product=product, user_made = self.request.user)

        return super().form_valid(form)


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
        context['all_products_suppliers'] = Supplier.objects.get_all_products(self.object)
        return context
    
