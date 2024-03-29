# Función para procesar un formulario individual
from decimal import Decimal
from django_afip.models import *
from django.contrib import messages
from django.shortcuts import redirect

from branches.utils import set_branch_session
from branches.models import Branch_Objetives
from django.utils import timezone
from clients.forms import *
from .models import *

now_utc = timezone.now()
now_local = timezone.localtime(now_utc)
fecha_hoy = now_local.date()
hora_actual = now_local.time()

def get_total_and_products(formset):
    """Segun los prodcutos recibidos, se suma un total $$. 
    A demas de guardar dichos productos en una varaible all_products_to_sale"""
    total = 0

    product = formset.cleaned_data['product']
    quantity = formset.cleaned_data['quantity']
    for _ in range(quantity):
        total += product.sale_price

    return total


def update_stock(formset):
    product = formset.cleaned_data['product']
    quantity = formset.cleaned_data['quantity']
    if not 'cristal' in product.category.name.lower() and not 'propio' in product.name.lower():
        product.stock -= quantity
    product.save()
    

def process_formset(formset, promotional_products, wo_promo):
    """Procesa el un producto que viene del formset y retorna un detalle de venta (order_detail)"""
    if formset.is_valid():
        product = formset.cleaned_data['product']
        quantity = formset.cleaned_data['quantity']
        discount = formset.cleaned_data['discount'] or 0

        price = product.sale_price

        order_detail = OrderDetail.objects.create(
            product=product, 
            quantity=quantity,
            price=price, 
            discount=discount)

        promotion = product.promotions.filter(promotion__is_active=True).exists()
        if promotion: # si tiene promo
            for _ in range(quantity):
                promotion = product.promotions.last().promotion
                promotional_products[promotion].append((product, discount))
        else:
            for _ in range(quantity):
                wo_promo.append(product.sale_price*Decimal(1-discount/100))

        return order_detail

# Función para calcular la suma de los primeros N elementos de una lista
def sumFirst_N_Elements(lst, n, reverse=True):
    lst = sorted(lst,reverse=reverse)
    return sum(lst[:n])

# Función para procesar productos en una promoción
def process_promotion(promotional_products, promotion, products_with_discountPromo, real_price_promo):
    discounted_prices = [] 

    list_products = []

    for elemento in products_with_discountPromo:
        if isinstance(elemento, tuple):
            list_products.append(elemento)
        else:
            percentage_desc_promo = elemento

    for product, discount in list_products: # _ SERIA EL DESCUENTO DE LA PROPIA PROMO
        original_price = product.sale_price
        discounted_price = original_price * Decimal(1 - (discount / 100))
        discounted_prices.append(discounted_price)

    # Actualiza la lista de productos en el diccionario con los precios finales
    promotional_products[promotion] = discounted_prices
    promotional_products[promotion].sort()

    if len(promotional_products[promotion]) > 1:
        if '2x1' in promotion.type_prom.name:
            quantity_elem = len(promotional_products[promotion])
            if quantity_elem % 2 != 0:
                quantity_elem = quantity_elem // 2 + 1
            else: 
                quantity_elem = quantity_elem // 2

            real_price_promo.append(sumFirst_N_Elements(promotional_products[promotion], quantity_elem))

        elif '2da' in promotion.type_prom.name:
            quantity_elem_org = len(promotional_products[promotion])
            if quantity_elem_org % 2 != 0:
                quantity_elem = quantity_elem_org // 2 + 1
            else: 
                quantity_elem = quantity_elem_org // 2

            total_sin_desc = sumFirst_N_Elements(promotional_products[promotion], quantity_elem)
            resto = sumFirst_N_Elements(promotional_products[promotion], quantity_elem_org-quantity_elem, False)
            resto = resto*(1-percentage_desc_promo/100)
            real_price_promo.append(total_sin_desc+resto)
            
        else: 
            real_price_promo.append(sum(promotional_products[promotion])*(1-percentage_desc_promo/100))

    elif 'Descuento' in promotion.type_prom.name and len(promotional_products[promotion]) > 0 : # Decuento unitario
        real_price_promo.append(sum(promotional_products[promotion])*(1-percentage_desc_promo/100))

    else:
        real_price_promo.append(sum(promotional_products[promotion]))
        
        
        

def switch_invoice_receipt(invoice_or_receipt, sale, pos_afip):
    """Dependiendo el tipo de FACTURA O COMPROBANTE, lo guarda y lo retorna para IMPRIMIR"""
    
    if invoice_or_receipt in ['A', 'B']:
        
        if invoice_or_receipt == 'A':
            document = DocumentType.objects.get(id=1)
            receipt_type = ReceiptType.objects.get(id=1)
            
            if len(sale.customer.dni) < 11:
                return 'Para factura A, el CUIT del cliente debe contener 11 digitos.'
        
        elif invoice_or_receipt == 'B':
            
            receipt_type = ReceiptType.objects.get(id=4)
            if len(sale.customer.dni) > 10:
                document = DocumentType.objects.get(id=2) #es cuil
            elif len(sale.customer.dni) < 2:
                document = DocumentType.objects.get(id=36) #es del tipo otro
            else:
                document = DocumentType.objects.get(id=10) #es dni
        
        receipt = Receipt.objects.create(
            point_of_sales = pos_afip,
            receipt_type = receipt_type,
            concept = ConceptType.objects.get(id=1),
            issued_date = fecha_hoy,
            document_type = document,
            document_number = sale.customer.dni,
            total_amount = sale.total,
            net_untaxed = 0,
            net_taxed = Decimal(sale.total / Decimal(1.21)),
            exempt_amount = 0,
            )
        sale.receipt = receipt
        sale.save()
        
        vat = Vat.objects.create(
            vat_type = VatType.objects.get(id=3), # 21%
            base_amount = sale.receipt.net_taxed,
            amount = Decimal(sale.receipt.total_amount - sale.receipt.net_taxed),
            receipt = sale.receipt
            ) 
        
        # Realiza la validación del recibo con la AFIP
        try:
            validation_result = sale.receipt.validate()
        except:
            vat.delete()
            receipt.delete()
            return 'Error de comunicacion con AFIP.'
        



def find_cristal_product(all_products_to_sale, sale=None):
    """Ecuentra un CRISTAL dentro de la orden de venta (productos)"""
    if sale:
        all_products_to_sale = Product.objects.filter(order_detaill__sale=sale)

    for product in all_products_to_sale:
        if 'cristal' in product.category.name.lower():
            return product
    return None

def find_contacto_product(all_products_to_sale, sale=None):
    """Ecuentra un CRISTAL dentro de la orden de venta (productos)"""
    if sale:
        all_products_to_sale = Product.objects.filter(order_detaill__sale=sale)

    for product in all_products_to_sale:
        if 'contacto' in product.category.name.lower():
            return product
    return None

def find_armazons_product(all_products_to_sale, sale=None):
    """Ecuentra un Armazon dentro de la orden de venta (productos)"""
    if sale:
        all_products_to_sale = Product.objects.filter(order_detaill__sale=sale, category__name__icontains='Armaz')
        return all_products_to_sale

    for product in all_products_to_sale:
        if any(keyword in product.category.name.lower() for keyword in ['armazón', 'armazon', 'armazones']):
            return product
    return None





def process_customer(customer, sale, payment_methods, total, product_cristal, product_contacto, amount, request):
    """
    Funcion que procesa los datos de metodos de pago y el tipo de cliente.
    """

    payment_total = 0
    if payment_methods.is_valid():
        if not customer:
            customer = Customer.objects.get(id=1)

        for methods in payment_methods:
            if methods.is_valid():
                payment_total += methods.cleaned_data['amount']
                
        # if payment_total >= total:
        #     payment = payment_total
        # else:
        #     payment = total - payment_total
        #     sale.missing_balance = payment
        
        if Decimal(total) - Decimal(payment_total) > 0:
            sale.state = Sale.STATE[1][0] # "PENDIENTE"
        else:
            sale.state = Sale.STATE[0][0] # "COMPLETO"
                    


        # Modificamos la forma de obtener la sucursal
        branch_actualy = set_branch_session(request)

        sale.branch = branch_actualy
        sale.user_made = request.user
        sale.customer = customer
        sale.save()
        
        missing_balance = total
        
        for methods in payment_methods:
            if methods.is_valid():
                method_amount = methods.cleaned_data['amount']
                
                mov = None
                
                missing_balance -= method_amount
                
                if customer and not 'consumidor' in customer.first_name.lower():
                    if customer.has_credit_account: # and 'cuenta corriente' in payment_methods.name.lower():
                        """Si el cliente TIENE CUENTA CORRIENTE + Metodo: CUENTA CORRIENTE"""
                        sale.state = Sale.STATE[0][0] # COMPLETADO
                        customer.credit_balance += total * Decimal(1 - sale.discount / 100)
                        customer.save()
                        
                        missing_balance = 0
                        sale.total = total
                        sale.save()

                    # elif customer.has_credit_account:
                    #     """Si TIENE CUENTA CORRIENTE + Metodo: Credito/Debito/Efectivo"""
                    #     missing_balance = Decimal(total) - Decimal(payment_total) # Diferencial total de la venta con el pago del cliente
                    #     sale.missing_balance = missing_balance
                    #     if missing_balance > 0:
                    #         customer.credit_balance += missing_balance
                    #         customer.save()
                    #     set_movement(payment_total, payment_methods.type_method, customer, request)

                    elif not customer.has_credit_account and product_cristal or product_contacto: 
                        """Si lo que el cliente NO TIENE CUENTA CORRIENTE compra tiene CRISTAL"""
                        # missing_balance += max(Decimal(0), Decimal(total) - Decimal(payment_total))
                        # sale.missing_balance = missing_balance
                        mov = set_movement(method_amount, methods.cleaned_data['payment_method'].type_method, customer, request)
                        sale.save()

                    else:
                        """Si el cliente NO CUENTA CORRIENTE - NO CRISTAL"""
                        mov = set_movement(method_amount, methods.cleaned_data['payment_method'].type_method, customer, request)
                else:
                    """Si el CLIETNE NO REGISTRA"""
                    mov = set_movement(method_amount,  methods.cleaned_data['payment_method'].type_method, None, request)

                
                
                Payment.objects.create(
                    user_made = request.user,
                    customer = customer,
                    amount = method_amount if method_amount > 0 else total,
                    payment_method = methods.cleaned_data['payment_method'],
                    description = f"Pago de venta Nro: {sale.pk}",
                    sale = sale,
                    movement = mov
                )
    sale.missing_balance = missing_balance
    sale.save()
    # payment_total = amount
    
    



def set_movement(total, type_method, customer, request):
    from cashregister.utils import create_in_movement
    
    description = "Venta de productos"
    if customer and not 'consumidor' in customer.first_name.lower():
        description += " a %s" % customer.get_full_name()

    # Modificamos la forma de obtener la sucursal
    branch_actualy = set_branch_session(request)
    
    mov = create_in_movement(branch_actualy, request.user, type_method, description, total)
    
    return mov


def process_service_order(request, customer):
    service_order = ServiceOrderForm(request.POST)
    correction_form = CorrectionForm(request.POST)
    material_form = MaterialForm(request.POST)
    color_form = ColorForm(request.POST)
    cristal_form = CristalForm(request.POST)
    tratamiento_form = TratamientForm(request.POST)
    pupilar_form = InterpupillaryForm(request.POST)

    if (
        service_order.is_valid() and
        correction_form.is_valid() and
        material_form.is_valid() and 
        color_form.is_valid() and
        cristal_form.is_valid() and 
        tratamiento_form.is_valid() and 
        pupilar_form.is_valid()
        ):
        # Create the main form instance
        service = ServiceOrder.objects.create_lab(
            request.user, service_order, correction_form, material_form,
            color_form, cristal_form, tratamiento_form, pupilar_form,
            customer
        )

    return service


def set_amounts_sale(sale, subtotal, wo_promo, real_price_promo, discount_sale, surcharge_sale):
    wo_promo = sum(wo_promo)
    real_price_promo = Decimal(sum(real_price_promo))

    sale.discount_extra = Decimal(subtotal - real_price_promo - wo_promo)
    sale.subtotal = Decimal(subtotal)
    sale.total = Decimal(real_price_promo + wo_promo) * Decimal(1 - discount_sale/100)
    # Calcular el total sin recargo
    total_without_surcharge = Decimal(real_price_promo + wo_promo) * Decimal(1 - discount_sale/100)

    # Calcular el recargo
    surcharge_amount = total_without_surcharge * Decimal(surcharge_sale/100)
    
    sale.total = round(total_without_surcharge + surcharge_amount, 2)


def up_objetives(employpee, sale):
    self_objetives = employpee.employee_objetives.filter(
        objetive__exp_date__gte=fecha_hoy)
    accumulate_objectives(self_objetives, sale)
    
    objetives = Branch_Objetives.objects.filter(objetive__exp_date__gte=fecha_hoy)
    accumulate_objectives(objetives, sale)

def accumulate_objectives(objetives, sale):
    for objetive in objetives:
        objetive.accumulated += sale.total
        objetive.save()