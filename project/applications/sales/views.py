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

        context['sale_form'] = SaleForm(branch = branch)

        context['branch_selected'] = branch.name
        context['customer_form'] = CustomerForm
        return context

    def form_valid(self, form):
        saleform = SaleForm(self.request.POST)

        promotions_active = Promotion.objects.filter(is_active=True)

        promotional_products = {promotion: [] for promotion in promotions_active}

        formsets = form
        # Procesa los datos del formulario aquí
        for formset in formsets:
            if formset.is_valid():
                product = formset.cleaned_data['product']
                quantity = formset.cleaned_data['quantity']
                discount = 0 if not formset.cleaned_data['discount'] else formset.cleaned_data['discount']

                promotion = product.promotions.last().promotion
                if promotion:
                    while quantity != 0:
                        promotional_products[promotion].append((product, discount))
                        quantity = quantity - 1

        # Ordena los productos en cada promoción por precio
        for promotion, products in promotional_products.items():
            discounted_prices = []
            print(products)

            for product, discount in products:
                original_price = product.sale_price
                discounted_price = original_price * Decimal(1 - (discount / 100))
                discounted_prices.append(discounted_price)

            # Actualiza la lista de productos en el diccionario con los precios finales
            promotional_products[promotion] = discounted_prices
            products = sorted(products, key=lambda product: product.sale_price)
        
        print('\n\n',promotional_products)
        
        messages.success(self.request, "Se ha generado la venta con éxito!")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Error. Verifique los datos.")
        return super().form_invalid(form)
