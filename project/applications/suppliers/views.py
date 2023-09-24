from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (UpdateView, DeleteView, ListView, DetailView, FormView,DeleteView)
from django.shortcuts import render

from applications.core.mixins import CustomUserPassesTestMixin
from .forms import SupplierForm
from .models import Supplier, Product_Supplier
#from .core.utils import obtener_nombres_de_campos
from applications.employes.utils import obtener_nombres_de_campos

# Create your views here.
class SupplierCreateView(CustomUserPassesTestMixin, FormView):
    form_class = SupplierForm
    template_name = 'suppliers/supplier_create_page.html'
    success_url = reverse_lazy('suppliers_app:list_supplier')

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
    template_name = 'suppliers/supplier_update_page.html'
    success_url = reverse_lazy('suppliers_app:list_supplier')

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
    template_name = 'suppliers/supplier_list_page.html'
    context_object_name = 'suppliers'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exclude_fields = ["id", "deleted_at", "created_at", "updated_at","phone_code"]
        context['table_column'] = obtener_nombres_de_campos(Supplier, *exclude_fields)
        return context


class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'suppliers/supplier_page.html'
    context_object_name = 'supplier'
    
    def get_object(self, queryset=None):
        # Intenta obtener el objeto Product o retorna None si no se encuentra
        try:
            obj = super().get_object(queryset=queryset)
        # Puedes retornar None o cualquier otro valor que desees
        except:
            obj=None
        return obj
        
    def get(self, request, *args, **kwargs):
        # Obtén el objeto utilizando el método get_object()
        self.object = self.get_object()
        
        if self.object is None:
            # El objeto no se encontró, renderiza una plantilla personalizada
            return render(request, 'suppliers/supplier_page.html')
        # El objeto se encontró, continúa con el comportamiento predeterminado
        context =self.get_context_data()
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_products_suppliers'] = Supplier.objects.get_all_products(self.object)
        return context

class SupplierDeleteView(CustomUserPassesTestMixin,DeleteView):
    model = Supplier
    template_name = 'suppliers/supplier_delete_page.html'
    success_url = reverse_lazy('suppliers_app:list_supplier')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Realiza la eliminación suave
        return HttpResponseRedirect(self.get_success_url())
