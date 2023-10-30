# Función para procesar un formulario individual
from decimal import Decimal
from django.contrib import messages

from project.settings.base import DATE_NOW
from applications.cashregister.models import CashRegister, Currency, Movement

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

    product.stock -= quantity
    product.save()
    return total


def process_formset(formset, promotional_products):
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
        if promotion:
            for _ in range(quantity):
                promotion = product.promotions.last().promotion
                promotional_products[promotion].append((product, discount))

        return order_detail

# Función para calcular la suma de los primeros N elementos de una lista
def sumFirst_N_Elements(lst, n):
    return sum(sorted(lst)[:n])

# Función para procesar productos en una promoción
def process_promotion(promotional_products, promotion, products_with_discountPromo, discount_promo):
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
                quantity_elem = quantity_elem // 2 - 1
            else: 
                quantity_elem = quantity_elem // 2

            discount_promo.append(sumFirst_N_Elements(promotional_products[promotion], quantity_elem))

        elif '2da' in promotion.type_prom.name:
            quantity_elem = len(promotional_products[promotion])
            if quantity_elem % 2 != 0:
                quantity_elem = quantity_elem // 2 - 1
            else: 
                quantity_elem = quantity_elem // 2

            discount_promo.append(sumFirst_N_Elements(promotional_products[promotion], quantity_elem)*(1-percentage_desc_promo/100))
        
        else: # Decuento unitario
            discount_promo.append(sum(promotional_products[promotion])*(percentage_desc_promo/100))


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

def find_cristal_product(all_products_to_sale):
    """Ecuentra un CRISTAL dentro de la orden de venta (productos)"""
    for product in all_products_to_sale:
        if 'cristal' in product.category.name.lower():
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

    if customer:
        if customer.has_credit_account and 'cuenta corriente' in payment_methods.__str__().lower():
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
            # set_movement(payment_total, payment_methods.type_method, customer, request)

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

    sale.branch = request.user.branch
    sale.user_made = request.user
    sale.save()

    Payment.objects.create(
        user_made = request.user,
        amount = amount if amount > 0 else total,
        payment_method = payment_methods,
        description = f"Pago de venta Nro: {sale.pk}",
        sale = sale,
    )


def set_movement(total, type_method, customer, request):
    description = "Venta de productos"
    if customer and not 'Anonimo' in customer.first_name:
        description += " a %s" % customer.get_full_name()

    # Modificamos la forma de obtener la sucursal
    branch_actualy = request.session.get('branch_actualy') or request.user.branch.pk
    branch_actualy = Branch.objects.get(id=branch_actualy)

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

        print(service)
    else: 
        print(correction_form.errors)