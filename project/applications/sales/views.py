from decimal import Decimal
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
from django.views.generic import ListView

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
        # context['payment_form'] = PaymentMethodsFormset
        context['branch_selected'] = branch.name
        context['customer_form'] = CustomerForm
        context['payment_method_form'] = PaymentMethodForm
        
        return context


    def form_valid(self, form):
        formsets = form
        saleform = SaleForm(self.request.POST)
        # payment_methods = PaymentMethodsFormset(self.request.POST)

        if saleform.is_valid():
            sale = saleform.save(commit=False)
            print('\n\n\nDatos de SaleForm: ',saleform.cleaned_data)
            customer = saleform.cleaned_data['customer']
            payment_methods = saleform.cleaned_data.pop('payment_method')
            amount = saleform.cleaned_data.pop('amount')
            general_discount = saleform.cleaned_data.pop('general_discount')
            if not customer:
                customer = Customer.objects.get(name__icontains='Anonimo') #'Anonimo'

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
 
        sale.discount = discount_promo + Decimal(total * general_discount/100)
        sale.total = total
        print('=> TOTAL: ', total - discount_promo)

        has_proof = saleform.cleaned_data.pop('has_proof') or None
        proof_type = switch_case(has_proof, sale)
        if proof_type:
            generate_proof(proof_type)

        product_cristal = find_cristal_product(all_products_to_sale)
        customer_cc_and_cristal = process_customer(customer, sale, payment_methods, total, product_cristal, amount, self.request.user)
        if customer_cc_and_cristal:
            # messages.info(self.request, "%s" % product_cristal.name)
            return HttpResponseRedirect(reverse_lazy('clients_app:service_order_new', kwargs={'pk': customer.pk}))

        messages.success(self.request, "Se ha generado la venta con éxito!")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Error. Verifique los datos.")
        return super().form_invalid(form)


class PaymentMethodCreateView(FormView):
    """
    Crear una catogoria nueva para el producto
    """
    form_class = PaymentMethodForm
    template_name = 'sales/payment_method_create_page.html'
    success_url = reverse_lazy('sales_app:payment_method_view')

    def form_valid(self, form):
        payment_method  = form.save(commit=False)
        payment_method.user_made = self.request.user
        payment_method.save()

        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest': # Para saber si es una peticion AJAX
            new_payment_method_data = {
                'id': payment_method.id,
                'name': payment_method.__str__(),
            }
            # Si es una solicitud AJAX, devuelve una respuesta JSON
            return JsonResponse({'status': 'success', 'new_payment_method': new_payment_method_data})
        else:
            # Si no es una solicitud AJAX, llama al método form_valid del padre para el comportamiento predeterminado
            return super().form_valid(form)
        
    def form_invalid(self, form):
        
        print("######################################################")
        print("El formulario es invalido")
        print(form.errors)
        print(form.cleaned_data['name'])
        print(form.cleaned_data.get('type_method'))
        return super().form_invalid(form)
    
    
class PaymentMethodView(ListView):
    """
    Listar todas las categorias de productos
    """
    model = PaymentMethod
    template_name = 'sales/payment_method_list_page.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment_method_form'] = PaymentMethodForm
        return context