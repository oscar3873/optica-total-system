import locale
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

#Importaciones de la app
from applications.branches.models import Branch
from applications.clients.forms import CustomerForm
from applications.promotions.models import Promotion
from applications.cashregister.utils import obtener_nombres_de_campos

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
                print('\n\nDatos de Formset: ', formset.cleaned_data)
                total += get_total_and_products(formset, all_products_to_sale)
                order_details.append(process_formset(formset, promotional_products))

                product_cristal = find_cristal_product(all_products_to_sale)
                if product_cristal and not customer:
                    messages.error(self.request, "Seleccione un cliente antes de Vender Cristales")
                    return super().form_invalid(form)

        # Ordena los productos en cada promoción por precio
        for promotion, products in promotional_products.items():
            process_promotion(promotional_products, promotion, products, discount_promo)
            
        discount_promo = sum(discount_promo)
        print('DESCUENTO TOTAL: ', discount_promo)

        sale.total = total
        print('=> TOTAL aplicando descuento: ', total - discount_promo)

        has_proof = saleform.cleaned_data.pop('has_proof') or None
        proof_type = switch_invoice_receipt(has_proof, sale)
        if proof_type:
            generate_proof(proof_type)

        process_customer(customer, sale, payment_methods, total, amount, self.request.user)

        for order in order_details:
            order.sale = sale
            order.save()

        if product_cristal:
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
    
    
######################## SALES #############################

class SalesListView(ListView):
    template_name = 'sales/sale_page.html'
    model = Sale
    paginate_by = 25
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí se recupera la caja de la sucursal correspondiente al usuario logueado
        try:
            branch_actualy = self.request.session.get('branch_actualy')
            branch_actualy = Branch.objects.get(id=branch_actualy)
            sales = Sale.objects.filter(branch=branch_actualy, deleted_at=None).order_by('-created_at')
        except CashRegister.DoesNotExist:
            sales = None
            messages.error(self.request, 'No hay ventas registradas para esta sucursal')
        context['sales'] = sales
        context['table_column'] = obtener_nombres_de_campos(Sale,
            "id",
            "invoice", 
            "receipt",
            "refund_date",
            "branch",
            "deleted_at", 
            "discount",
            "created_at",
            "updated_at", 
            )
        
        return context
    

#------- VISTAS BASADAS EN FUNCIONES PARA PETICIONES AJAX -------#

################ SEARCH MOVEMENTS AJAX ################

def ajax_search_sales(request):
    # branch = request.user.branch

    # branch_actualy = request.session.get('branch_actualy')
    # if request.user.is_staff and branch_actualy:
    #     branch = Branch.objects.get(id=branch_actualy)

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

        # Obtener el valor de search_term de la solicitud
        search_term = request.GET.get('search_term', '')
        print("###################### Esto es lo que se esta buscando: ",search_term)
        if not search_term:
            # En caso de que search_term esté vacío, muestra la cantidad de empleados por defecto
            paginate_by = SalesListView().paginate_by
            print("####################################",paginate_by)
            sales = Sale.objects.all().filter(deleted_at = None)[:paginate_by]
        else:
            # Usando Q por todos los campos existentes en la tabla
            sales = Sale.objects.all().filter(deleted_at = None).filter(
                Q(total__icontains=search_term) |
                Q(date_time_sale__icontains=search_term) |
                Q(state__icontains=search_term) |
                Q(user_made__first_name__icontains=search_term) |
                Q(user_made__last_name__icontains=search_term) |
                Q(customer__first_name__icontains=search_term) |
                Q(customer__last_name__icontains=search_term)
            )[:25]
        # Crear una lista de diccionarios con los datos de los empleados
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        data = [{
            'id': sale.id,
            'total': sale.total,
            'missing_balance': sale.missing_balance,
            'date_time_sale': sale.date_time_sale.strftime('%d %B %Y'),
            'state': sale.state,
            'customer': str(sale.customer),
            'customer_id': sale.customer.id,
            'user_made': str(sale.user_made),
            'is_staff': 1 if request.user.is_staff else 0
        } for sale in sales]
        locale.setlocale(locale.LC_TIME, '')
        return JsonResponse({'data': data})