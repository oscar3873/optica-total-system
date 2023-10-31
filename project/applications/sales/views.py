import copy
from datetime import datetime
import locale
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic import *
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

#Importaciones de la app
from applications.branches.models import Branch
from applications.clients.forms import *
from applications.promotions.models import Promotion
from applications.cashregister.utils import obtener_nombres_de_campos
from applications.core.mixins import CustomUserPassesTestMixin

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

        context['order_servise'] = {
            'service': ServiceOrderForm,
            'pupilar': InterpupillaryForm,
            'correction': CorrectionForm,
            'material': MaterialForm,
            'color': ColorForm,
            'cristal': CristalForm,
            'tratamiento': TratamientForm,
        }
        
        return context

    @transaction.atomic
    def form_valid(self, form):
        formsets = form
        saleform = SaleForm(self.request.POST)
        # payment_methods = PaymentMethodsFormset(self.request.POST)

        branch_actualy = self.request.session.get('branch_actualy') or self.request.user.branch.pk
        branch_actualy = Branch.objects.get(id=branch_actualy)

        if saleform.is_valid():
            sale = saleform.save(commit=False)
            customer = saleform.cleaned_data['customer']
            payment_methods = saleform.cleaned_data.pop('payment_method')
            amount = saleform.cleaned_data.pop('amount')
            discount_sale = saleform.cleaned_data['discount']
            if discount_sale < 0:
                messages.error(self.request, "Descuento de venta Inválido. Ingrese solo valores positivos.")
                return super().form_invalid(form)

        promotions_active = Promotion.objects.filter(is_active=True, branch=branch_actualy, deleted_at=None)
        promotional_products = {promotion: [(promotion.discount)] for promotion in promotions_active}

        
        order_details = []
        all_products_to_sale = []
        real_price_promo = []
        subtotal = 0

        # Procesa los datos del formset
        for formset in formsets:
            if not formset.cleaned_data['product']:
                messages.error(self.request, "No se ha seleccionado ningun producto.")
                return super().form_invalid(form)
            
            if formset.is_valid():
                subtotal += get_total_and_products(formset, all_products_to_sale)

                product_cristal = find_cristal_product(all_products_to_sale)
                if product_cristal and not customer:
                    messages.error(self.request, "Seleccione un cliente antes de Vender Cristales")
                    return super().form_invalid(form)
                order_details.append(process_formset(formset, promotional_products))
                
                

        promotional_products_clone = copy.copy(promotional_products)
        # Ordena los productos en cada promoción por precio
        for promotion, products_with_discountPromo in promotional_products.items():
            process_promotion(promotional_products_clone, promotion, products_with_discountPromo, real_price_promo)
        
        print('\n\n\nLISTADO DE PROMOCIONES: ', promotional_products_clone, '\n')
        print('LISTADO DE PRECIOS A COBRAR POR PROMO: ', real_price_promo)
        real_price_promo = Decimal(sum(real_price_promo))
        print('SUBTOTAL (TOTAL EN PRODUCTOS): ', subtotal)
        print('DESCUENTO TOTAL: ', subtotal - real_price_promo)
        print('DESCUENTO DE VENTA: %', discount_sale)
        sale.discount_extra = subtotal - real_price_promo
        sale.subtotal = Decimal(real_price_promo)
        sale.total = Decimal(real_price_promo) * Decimal(1 - discount_sale/100)
        print('=> TOTAL aplicando descuento: ', sale.total, '\n\n')

        if product_cristal and amount < sale.total/2: # Se lleva un cristal o lente de contacto, pero el monto pagado es menor al 50%
            messages.error(self.request, "El pago debe ser mayor al 50% del total.")
            return super().form_invalid(form)
        
        has_proof = saleform.cleaned_data.pop('has_proof') or None
        proof_type = switch_invoice_receipt(has_proof, sale)
        if proof_type:
            generate_proof(proof_type)

        process_customer(customer, sale, payment_methods, sale.total, product_cristal, amount, self.request)

        for order in order_details:
            order.sale = sale
            order.save()

        if product_cristal and not 'anonimo' in customer.first_name.lower():
            service_order = process_service_order(self.request, customer)
            service_order.sale = sale
            service_order.save()
            # renderizar html de service_order sin return para que continue la funcion form_valid
        
        messages.success(self.request, "Se ha generado la venta con éxito!")
        return HttpResponseRedirect(reverse_lazy('sales_app:sale_detail_view', kwargs={'pk': sale.id}))

    def form_invalid(self, form):
        print(form.errors)
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
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message':'Ya existe el Metodo de Pago.'})
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
            "subtotal",
            )
        
        return context
    

class SaleDetailView(CustomUserPassesTestMixin, DetailView):
    template_name = 'sales/sale_detail_page.html'
    model = Sale
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #detalles de venta en la venta que viene por url
        context['sale'] = Sale.objects.get(id=self.kwargs['pk'])
        context['sale_subtotal'] = context['sale'].subtotal
        context['sale_discount_amount'] = context['sale_subtotal'] * Decimal(context['sale'].discount/100)
        context['sale_total'] = context['sale_subtotal'] - context['sale_discount_amount']
        # Ordenes de detalle de la venta ...
        context['sale_details'] = OrderDetail.objects.filter(sale=context['sale'])
        return context

#------- VISTAS BASADAS EN FUNCIONES PARA PETICIONES AJAX -------#

def show_invoice(request, pk):
    sale = Sale.objects.get(id=pk)
    customer = sale.customer

    try:
        service_order = ServiceOrder.objects.get(sale=sale, is_done=False)
    except ServiceOrder.DoesNotExist:
        service_order = None

    payment = Payment.objects.get(sale=sale)

    order_details = sale.order_detaill.filter(sale=sale)
    order_details_template = []
    subtotal = []

    for order in list(order_details):
        order_details_template.append((order, f'{Decimal(order.price)*Decimal(1-order.discount/100):.2f}'))
        subtotal.append( order.price * order.quantity)

    # Convertir la cadena en un objeto de fecha
    locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

    format = "%A, %d de %B de %Y"
    sale_date_str = sale.created_at.strftime(format)

    context = {
        'customer': customer,
        'total': f'{sale.total:.2f}',  # Muestra sale.total con 2 decimales
        'order_details': order_details_template,
        'subtotal': sum(subtotal),
        'service_order': service_order if service_order else None,  # Incluye service_order solo si no es None
        'od_lejos': f'{service_order.correction.lej_od_esferico} {service_order.correction.lej_od_cilindrico} {service_order.correction.lej_od_eje}' if service_order else None,
        'oi_lejos': f'{service_order.correction.lej_oi_esferico} {service_order.correction.lej_oi_cilindrico} {service_order.correction.lej_oi_eje}' if service_order else None,
        'od_cerca': f'{service_order.correction.cer_od_esferico} {service_order.correction.cer_od_cilindrico} {service_order.correction.cer_od_eje}' if service_order else None,
        'oi_cerca': f'{service_order.correction.cer_oi_esferico} {service_order.correction.cer_oi_cilindrico} {service_order.correction.cer_oi_eje}' if service_order else None,
        'seler': sale.user_made,
        'promo': f'{sale.total}',
        'discount': f'{sale.discount:.2f}',
        'discount_extra': f'{sale.discount_extra:.2f}',
        'payment_method': payment.payment_method.name,
        'pay': f'{sale.total - sale.missing_balance:.2f}',
        'missing_balance': f'{sale.missing_balance:.2f}',  # Saldo pendiente
        'date': sale_date_str,
        'time': sale.created_at.time()
    }

    return render(request, 'sales/components/comprobante_pago.html', context)


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