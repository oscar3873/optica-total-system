from typing import Any
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (UpdateView, DeleteView, ListView, DetailView, FormView,DeleteView)
from django.shortcuts import render

from applications.core.mixins import CustomUserPassesTestMixin
from .forms import BankForm, SupplierForm
from .models import *
#from .core.utils import obtener_nombres_de_campos
from applications.employes.utils import obtener_nombres_de_campos

# Create your views here.
class SupplierCreateView(CustomUserPassesTestMixin, FormView):
    form_class = SupplierForm
    template_name = 'suppliers/supplier_create_page.html'
    success_url = reverse_lazy('suppliers_app:list_supplier')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bank_form'] = BankForm
        context['update_create'] = 'Registrar un proveedor'
        return context

    def form_valid(self, form):
        supplier = form.save(commit=False)
        supplier.user_made = self.request.user
        supplier.save()
        
        for brand in form.cleaned_data['brands']:
            Brand_Supplier.objects.create(supplier=supplier, brand=brand)
        return super().form_valid(form)


class SupplierUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_create_page.html'
    success_url = reverse_lazy('suppliers_app:list_supplier')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bank_form'] = BankForm
        context['update_create'] = f'Actualizar proveedor: {self.get_object().name.upper()}'
        return context

    def form_valid(self, form):
        form.instance.user_made = self.request.user
        supplier = form.save()

        selected_brands = form.cleaned_data['brand']
        existing_brands = supplier.brand_suppliers.all()

        # Elimina relaciones existentes que ya no están seleccionadas
        for brand_suppliers in existing_brands: # brand_suppliers es la tabla intermedia (relacion inversa)
            if brand_suppliers.brand not in selected_brands:
                supplier.brand_suppliers.get(brand=brand_suppliers.brand).delete()

        # Crea nuevas relaciones solo para características no existentes
        for brand in selected_brands:
            if brand not in existing_brands.values_list('brand', flat=True): # Si NO existe ya un producto relacionado con el proveedor, crea la relacion
                Brand_Supplier.objects.create(supplier=supplier, brand=brand, user_made = self.request.user)

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


from django.shortcuts import render
from django.views.generic import DetailView

class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'suppliers/supplier_page.html'
    context_object_name = 'supplier'
    
    def get_object(self, queryset=None):
        # Intenta obtener el objeto Supplier o retorna None si no se encuentra
        try:
            obj = super().get_object(queryset=queryset)
        except:
            obj = None
        return obj
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier = self.object  # Obtén el proveedor del contexto
        
        # Obtén las marcas relacionadas al proveedor
        brands = supplier.brand_suppliers.all()
        
        context['related_brands'] = brands
        return context

class SupplierDeleteView(CustomUserPassesTestMixin,DeleteView):
    model = Supplier
    template_name = 'suppliers/supplier_delete_page.html'
    success_url = reverse_lazy('suppliers_app:list_supplier')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Realiza la eliminación suave
        return HttpResponseRedirect(self.get_success_url())


def set_bank_supplier(request):
    if request.method == 'POST':
        bank_form = BankForm(request.POST)
        if bank_form.is_valid():
            supplier_id = request.POST.get('supplier_id')  # Asegúrate de tener el campo supplier_id en tu formulario
            supplier = Supplier.objects.get(pk=supplier_id)
            bank = bank_form.save(commit=False)
            bank.user_made = request.user
            bank.supplier = supplier
            bank.save()

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                bank_data = {
                    'id': bank.pk,
                    'name': bank.bank_name,
                    'cbu': bank.cbu,
                    'cuit': bank.cuit
                }
                return JsonResponse(bank_data)

    return JsonResponse({'error': 'No se pudo guardar el banco'})

def ajax_search_brands(request):
    search_term = request.GET.get('search_term', '')
    results = Brand.objects.filter(name__icontains=search_term).values('id', 'name')  # Filtrar las marcas que coincidan con el término de búsqueda
    return JsonResponse({'data': list(results)})