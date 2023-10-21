from decimal import Decimal
from django.http import HttpResponseRedirect
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

#Importaciones de la app
from applications.branches.models import Branch
from applications.clients.forms import CustomerForm
from applications.promotions.models import Promotion
from .utils import *
from .models import *
from .forms import *

# Create your views here.

class PointOfSaleView(LoginRequiredMixin, FormView):
    form_class = OrderDetailFormset
    template_name = 'sales/point_of_sale_page.html'
    success_url = reverse_lazy('core_app:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            branch_actualy = self.request.session.get('branch_actualy')
            branch = Branch.objects.get(id=branch_actualy)
        except Branch.DoesNotExist:
            branch = self.request.user.branch

        context['sale_form'] = SaleForm

        context['branch_selected'] = branch.name
        context['customer_form'] = CustomerForm
        return context

    def form_valid(self, form):
        formsets = form
        saleform = SaleForm(self.request.POST)

        if saleform.is_valid():
            sale = saleform.cleaned_data

        promotions_active = Promotion.objects.filter(is_active=True)
        promotional_products = {promotion: [] for promotion in promotions_active}

        order_details = []
        total = 0

        # Procesa los datos del formulario aquí
        for formset in formsets:
            if formset.is_valid():
                product = formset.cleaned_data['product']
                quantity = formset.cleaned_data['quantity']
                for _ in range(quantity):
                    total += product.sale_price

                order_details.append(process_formset(formset, promotional_products))
                
        discount_promo = []
        # Ordena los productos en cada promoción por precio
        for promotion, products in promotional_products.items():
            process_promotion(promotional_products, promotion, products, discount_promo)
            
        discount_promo = sum(discount_promo)
        print('DESCUENTO TOTAL: ', discount_promo)

        if saleform.cleaned_data['total'] == total:
            sale = saleform.save(commit=False)
            sale.total -= discount_promo 
            print(sale.total)

        messages.success(self.request, "Se ha generado la venta con éxito!")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Error. Verifique los datos.")
        return super().form_invalid(form)
