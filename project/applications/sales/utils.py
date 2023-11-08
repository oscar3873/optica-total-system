# Función para procesar un formulario individual
from decimal import Decimal

from applications.cashregister.models import CashRegister, Currency, Movement
from applications.branches.models import Branch_Objetives
from project.settings.base import DATE_NOW
from applications.clients.forms import *
from .models import *

def get_total_and_products(formset, all_products_to_sale):
    """Segun los prodcutos recibidos, se suma un total $$. 
    A demas de guardar dichos productos en una varaible all_products_to_sale"""
    total = 0

    product = formset.cleaned_data['product']
    all_products_to_sale.append(product)
    quantity = formset.cleaned_data['quantity']
    for _ in range(quantity):
        total += product.sale_price

    print(product.category.name)
    if not 'cristal' in product.category.name.lower() and not 'contacto' in product.category.name.lower():
        product.stock -= quantity
    product.save()
    return total


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

        promotion = product.promotions.exists()
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
            print('2x1')
            quantity_elem = len(promotional_products[promotion])
            if quantity_elem % 2 != 0:
                quantity_elem = quantity_elem // 2 + 1
            else: 
                quantity_elem = quantity_elem // 2

            real_price_promo.append(sumFirst_N_Elements(promotional_products[promotion], quantity_elem))

        elif '2da' in promotion.type_prom.name:
            print('2da1')
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
        

def switch_invoice_receipt(invoice_or_receipt, sale):
    """Dependiendo el tipo de FACTURA O COMPROBANTE, lo guarda y lo retorna para IMPRIMIR"""
    if invoice_or_receipt == 'A':
        return sale.invoice.create( # CREA UN OBJ DE FACTURA A
            # consultar Campos
        )
    elif invoice_or_receipt == 'B':
        return sale.invoice.create( # CREA UN OBJ DE FACTURA B
            # consultar Campos
        )
    elif invoice_or_receipt == 'C':
        return sale.receipt.create( # CREA UN OBJ DE COMPROBANTE / TICKET COMUN
            # consultar Campos
        )
    else:
        return None

def find_cristal_product(all_products_to_sale, sale=None):
    """Ecuentra un CRISTAL dentro de la orden de venta (productos)"""
    if sale:
        all_products_to_sale = Product.objects.filter(order_detaill__sale=sale)

    for product in all_products_to_sale:
        if 'cristal' in product.category.name.lower() or 'contacto' in product.category.name.lower():
            return product
    return None

def find_armazons_product(all_products_to_sale, sale=None):
    """Ecuentra un Armazon dentro de la orden de venta (productos)"""
    if sale:
        all_products_to_sale = Product.objects.filter(order_detaill__sale=sale, category__name__icontains='Armazon')
        return all_products_to_sale

    for product in all_products_to_sale:
        if 'armazon' in product.category.name.lower():
            return product
    return None

def generate_proof(proof_type): # generar factura o recibo
    print('IMPRIMIENDO %s' % proof_type)


def process_customer(customer, sale, payment_methods, total, product_cristal, amount, request):
    """
    Funcion que procesa los datos de metodos de pago y el tipo de cliente.
    """

    payment_total = 0
    # for payment in payment_methods:
    #     payment.save(commit=False)
    #     payment_total += payment.amount

    payment_total = amount

    if Decimal(total) - Decimal(payment_total) > 0:
        sale.state = Sale.STATE[1][0] # "PENDIENTE"
    else:
        sale.state = Sale.STATE[0][0] # "COMPLETO"

    if not customer:
        customer = Customer.objects.get(id=1)

    if customer and not 'consumidor' in customer.first_name.lower():
        if customer.has_credit_account and 'cuenta corriente' in payment_methods.name.lower():
            """Si el cliente TIENE CUENTA CORRIENTE + Metodo: CUENTA CORRIENTE"""
            customer.credit_balance += total * Decimal(1 - sale.discount / 100)
            customer.save()

        elif customer.has_credit_account:
            """Si TIENE CUENTA CORRIENTE + Metodo: Credito/Debito/Efectivo"""
            missing_balance = Decimal(total) - Decimal(payment_total) # Diferencial total de la venta con el pago del cliente
            sale.missing_balance = missing_balance
            if missing_balance > 0:
                customer.credit_balance += missing_balance
                customer.save()
            set_movement(payment_total, payment_methods.type_method, customer, request)

        elif product_cristal: 
            """Si lo que el cliente NO TIENE CUENTA CORRIENTE compra tiene CRISTAL"""
            missing_balance = Decimal(total) - Decimal(payment_total) # Diferencial total de la venta con el pago del cliente
            sale.missing_balance = missing_balance
            set_movement(payment_total, payment_methods.type_method, customer, request)

        else:
            """Si el cliente NO CUENTA CORRIENTE pero paga el total de la compra - NO CRISTAL"""
            set_movement(total, payment_methods.type_method, customer, request)
    else:
        """Si el CLIETNE NO REGISTRA"""
        set_movement(total,  payment_methods.type_method, None, request)

    # Modificamos la forma de obtener la sucursal
    from applications.branches.utils import set_branch_session
    branch_actualy = set_branch_session(request)

    sale.branch = branch_actualy
    sale.user_made = request.user
    sale.customer = customer
    sale.save()

    Payment.objects.create(
        user_made = request.user,
        amount = payment_total if payment_total > 0 else total,
        payment_method = payment_methods,
        description = f"Pago de venta Nro: {sale.pk}",
        sale = sale,
    )


def set_movement(total, type_method, customer, request):
    description = "Venta de productos"
    if customer and not 'consumidor' in customer.first_name.lower():
        description += " a %s" % customer.get_full_name()

    # Modificamos la forma de obtener la sucursal
    from applications.branches.utils import set_branch_session
    branch_actualy = set_branch_session(request)

    Movement.objects.create(
        user_made = request.user,
        payment_method = type_method,
        amount = total,
        cash_register = CashRegister.objects.filter(
            is_close = False,
            branch = branch_actualy,
            ).last(),
        description = description,
        currency = Currency.objects.first(),
        type_operation = "Ingreso",
    )


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

    print(service_order.errors,
    correction_form.errors,
    material_form.errors,
    color_form.errors,
    cristal_form.errors,
    tratamiento_form.errors,
    pupilar_form.errors)

    return service


def set_amounts_sale(sale, subtotal, wo_promo, real_price_promo, discount_sale):
    wo_promo = sum(wo_promo)
    real_price_promo = Decimal(sum(real_price_promo))

    sale.discount_extra = subtotal - real_price_promo
    sale.subtotal = Decimal(subtotal)
    sale.total = Decimal(real_price_promo + wo_promo) * Decimal(1 - discount_sale/100)


def up_objetives(user, sale):
    if not user.is_staff: # es empleado
        self_objetives = user.employee_type.employee_objetives.filter(is_completed=False, objetive__exp_date__lte=DATE_NOW.date())
        accumulate_objectives(self_objetives, sale)
        
        objetives = Branch_Objetives.objects.filter(is_completed=False, objetive__exp_date__lte=DATE_NOW.date())
        accumulate_objectives(objetives, sale)

def accumulate_objectives(objetives, sale):
    for objetive in objetives:
        if not objetive.is_completed:
            objetive.accumulated += sale.total
            objetive.save()