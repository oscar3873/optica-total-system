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
        context['payment_form'] = PaymentMethodsFormset
        context['branch_selected'] = branch.name
        context['customer_form'] = CustomerForm
        return context

    def form_valid(self, form):
        formsets = form
        saleform = SaleForm(self.request.POST)
        payment_methods = PaymentMethodsFormset(self.request.POST)

        if saleform.is_valid():
            sale = saleform
            print('\n\n\nDatos de SaleForm: ',saleform.cleaned_data)
            customer = saleform.cleaned_data['customer']
            if not customer:
                customer = Customer.objects.first()

        promotions_active = Promotion.objects.filter(is_active=True)
        promotional_products = {promotion: [] for promotion in promotions_active}

        order_details = []
        all_products_to_sale = []
        discount_promo = []
        total = 0

        # Procesa los datos del formset
        for formset in formsets:
            if not formset.cleaned_data['product']:
                messages.error(self.request, "No se ha seleccionado ningun producto.")
                return super().form_invalid(form)
            
            if formset.is_valid():
                total += get_total_and_products(formset, all_products_to_sale)
                order_details.append(process_formset(formset, promotional_products))

        # Ordena los productos en cada promoción por precio
        for promotion, products in promotional_products.items():
            process_promotion(promotional_products, promotion, products, discount_promo)
            
        discount_promo = sum(discount_promo)
        print('DESCUENTO TOTAL: ', discount_promo)

        sale = saleform.save(commit=False)
        sale.discount = discount_promo
        print('=> TOTAL: ', total - discount_promo)


        has_proof = saleform.cleaned_data.pop('has_proof') or None
        # proof_type = switch_case(has_proof, sale)
        # if proof_type:
        #     generate_proof(proof_type)

        product_cristal = True #find_cristal_product(all_products_to_sale)

        process_customer(customer, sale, payment_methods, total, product_cristal)
        if product_cristal:
            # messages.info(self.request, "%s" % product_cristal.name)
            return HttpResponseRedirect(reverse_lazy('clients_app:service_order_new', kwargs={'pk': customer.pk}))

        messages.success(self.request, "Se ha generado la venta con éxito!")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Error. Verifique los datos.")
        return super().form_invalid(form)
