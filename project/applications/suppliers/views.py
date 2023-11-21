from typing import Any
from django.http import Http404
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, ListView, DetailView, FormView,DeleteView
from django.contrib import messages

from applications.core.mixins import CustomUserPassesTestMixin
from .forms import *
from .models import *
#from .core.utils import obtener_nombres_de_campos
from applications.employes.utils import obtener_nombres_de_campos

# Create your views here.
################################# CREATE ##############################
class SupplierCreateView(CustomUserPassesTestMixin, FormView):
    form_class = SupplierForm
    template_name = 'suppliers/supplier_create_page.html'
    success_url = reverse_lazy('suppliers_app:list_supplier')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brandsSelected'] = Brand.objects.all()  # Obtén todas las marcas
        context['bank_form'] = CBUForm
        context['bank'] = BankForm
        context['update_create'] = 'Registrar un proveedor'
        return context

    def form_valid(self, form):
        supplier = form.save(commit=False)
        supplier.user_made = self.request.user
        supplier.save()

        banks = form.cleaned_data.get('cbu')
        for bank in banks:
            Supplier_Bank.objects.create(
                supplier=supplier,
                bank=bank,
                user_made=self.request.user
            )

        selected_brands = form.cleaned_data.get('brandsSelected')
        for brand in selected_brands:  # Usa brandsSelected en lugar de brands
            Brand_Supplier.objects.create(
                supplier=supplier, 
                brand=brand, 
                user_made=self.request.user
            )
        
        return super().form_valid(form)


################################# UPDATE ##############################
class SupplierUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_create_page.html'
    success_url = reverse_lazy('suppliers_app:list_supplier')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        supplier = self.get_object()
        related_brands = supplier.brand_suppliers.values_list('brand', flat=True)
        avaliable_brands = Brand.objects.filter(id__in=related_brands)
        
        context['brandsSelected'] = avaliable_brands  # Obtén todas las marcas
        context['cbus'] = Cbu.objects.filter(suppliers__supplier=supplier)
        context['bank_form'] = CBUForm
        context['bank'] = BankForm
        context['update_create'] = f'Actualizar proveedor: {supplier.name.upper()}'
        return context

    def form_valid(self, form):
        form.instance.user_made = self.request.user
        supplier = form.instance

        banks = form.cleaned_data.get('cbu')
        for bank in banks:
            Supplier_Bank.objects.create(
                supplier=supplier,
                bank=bank,
                user_made=self.request.user
            )

        selected_brands = form.cleaned_data['brandsSelected']  # Usa brandsSelected en lugar de brands
        existing_brands = supplier.brand_suppliers.all()

        for brand_suppliers in existing_brands:  # brand_suppliers es la tabla intermedia (relación inversa)
            if brand_suppliers.brand not in selected_brands:
                brand_suppliers.delete()

        for brand in selected_brands:
            if not supplier.brand_suppliers.filter(brand=brand).exists():
                Brand_Supplier.objects.create(supplier=supplier, brand=brand, user_made=self.request.user)

        supplier.save()
        
        return HttpResponseRedirect(reverse_lazy('suppliers_app:supplier_detail', kwargs = {'pk':supplier.pk}))
    
 
class BankUpdateView(UpdateView):
    model = Cbu
    form_class = CBUForm
    template_name = 'suppliers/cbu_update_page.html'
    context_object_name = 'cbu'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bank'] = BankForm
        return context

    def get_success_url(self):
        self.kwargs['pk_s']
        return reverse_lazy('suppliers_app:supplier_detail', kwargs = {'pk':self.kwargs['pk_s']})
    

################################# LIST ##############################
class SuppliersListView(CustomUserPassesTestMixin, ListView):
    model = Supplier
    template_name = 'suppliers/supplier_list_page.html'
    context_object_name = 'suppliers'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exclude_fields = ["id", "deleted_at", "created_at", "updated_at","phone_code","user_made"]
        context['table_column'] = obtener_nombres_de_campos(Supplier, *exclude_fields)
        return context


################################# DETAIL ##############################
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

################################# DELETE ##############################
class SupplierDeleteView(CustomUserPassesTestMixin,DeleteView):
    model = Supplier
    template_name = 'suppliers/supplier_delete_page.html'
    success_url = reverse_lazy('suppliers_app:list_supplier')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Realiza la eliminación suave
        return HttpResponseRedirect(self.get_success_url())


################################# AJAX #################################
def set_bank_supplier(request):
    if request.method == 'POST':
        bank_form = CBUForm(request.POST)
        if bank_form.is_valid():
            bank = bank_form.save(commit=False)
            bank.user_made = request.user
            bank.save()

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                bank_data = {
                    'id': bank.pk,
                    'name': bank.bank.bank_name,
                    'cbu': bank.cbu,
                    'cuit': bank.cuit
                }
                return JsonResponse({'status':'success', 'data': bank_data})
        print(bank_form.errors.as_json())
        return JsonResponse({'error': bank_form.errors.as_json()})
    return JsonResponse({'error': 'Por favor, verifique los campos.'})


def ajax_new_bank(request):
    if request.method == 'POST':
        bank_form = BankForm(request.POST)
        if bank_form.is_valid():
            bank = bank_form.save()
            bank_data = {
                'id': bank.pk,
                'name': bank.bank_name,
            }
            return JsonResponse({'status': 'success', 'bank_data': bank_data})
        else:
            error = bank_form.errors.get('bank_name', [None])[0]
            return JsonResponse({'error': error})
    else:
        error = 'Método de solicitud no válido.'
    return JsonResponse({'error': error})


def ajax_search_brands(request):
    search_term = request.GET.get('search_term', '')
    results = Brand.objects.filter(name__icontains=search_term).values('id', 'name')  # Filtrar las marcas que coincidan con el término de búsqueda
    return JsonResponse({'data': list(results)})


def ajax_delete_bank(request, pk):
    if request.method == 'POST':
        try:
            cbu = Cbu.objects.get(id=pk)
            cbu.suppliers.delete()
            cbu.delete()
            return JsonResponse({'status': 'success'})
        except Cbu.DoesNotExist:
            return JsonResponse({'error':'El ID no corresponde a ninguna Cuenta Bancaria'})