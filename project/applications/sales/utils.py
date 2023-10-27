# Función para procesar un formulario individual
from decimal import Decimal
from django.contrib import messages

from project.settings.base import DATE_NOW
from applications.cashregister.models import CashRegister, Currency, Movement, Transaction
from django.contrib import messages

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
    return total

def process_formset(formset, promotional_products):
    """Procesa el un producto que viene del formset y retorna un detalle de venta (order_detail)"""
    if formset.is_valid():
        product = formset.cleaned_data['product']
        quantity = formset.cleaned_data['quantity']
        discount = formset.cleaned_data['discount'] or 0

        price = product.sale_price * Decimal((1 + discount/100))

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
def process_promotion(promotional_products, promotion, products, discount_promo):
    discounted_prices = []

    for product, discount in products:
        original_price = product.sale_price
        discounted_price = original_price * Decimal(1 - (discount / 100))
        discounted_prices.append(discounted_price)

    # Actualiza la lista de productos en el diccionario con los precios finales
    promotional_products[promotion] = discounted_prices
    promotional_products[promotion].sort()

    if len(promotional_products[promotion]) > 1:
        quantity_elem = len(promotional_products[promotion])
        if quantity_elem % 2 != 0:
            quantity_elem = quantity_elem // 2 - 1
        else: 
            quantity_elem = quantity_elem // 2

        discount_promo.append(sumFirst_N_Elements(promotional_products[promotion], quantity_elem))
        """
        discount_promo = [ $, $, $ ...]
        """

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


def process_customer(customer, sale, payment_methods, total, product_cristal, amount, user):
    """
    Funcion que procesa los datos de metodos de pago y el tipo de cliente.
    """

    payment_total = 0
    # for payment in payment_methods:
    #     payment.save(commit=False)
    #     payment_total += payment.amount

    payment_total = amount

    if customer:
        if customer.has_credit_account and 'cuenta corriente' in payment_methods.__str__().lower():
            """Si el cliente TIENE CUENTA CORRIENTE + Metodo: CUENTA CORRIENTE"""
            sale.state = Sale.STATE[1][0] # "PENDIENTE"
            customer.credit_balance += total * Decimal(1 - sale.discount / 100)
            customer.save()

        elif customer.has_credit_account:
            """Si TIENE CUENTA CORRIENTE + Metodo: Credito/Debito/Efectivo"""
            missing_balance = Decimal(total) - Decimal(payment_total) # Diferencial total de la venta con el pago del cliente
            sale.missing_balance = missing_balance
            if missing_balance > 0:
                sale.state = Sale.STATE[1][0] # "PENDIENTE"
                customer.credit_balance += missing_balance
                customer.save()
            else:
                sale.state = Sale.STATE[0][0] # "COMPLETO"
            # set_movement(payment_total, payment_methods.type_method, customer, user)

        elif product_cristal: 
            """Si lo que el cliente NO TIENE CUENTA CORRIENTE compra tiene CRISTAL"""
            sale.state = Sale.STATE[1][0] # "PENDIENTE"
            missing_balance = Decimal(total) - Decimal(payment_total) # Diferencial total de la venta con el pago del cliente
            sale.missing_balance = missing_balance
            # set_movement(payment_total, payment_methods.type_method, customer, user)

        else:
            """Si el cliente TIENE O NO CUENTA CORRIENTE pero paga el total de la compra - NO CRISTAL"""
            sale.state = Sale.STATE[0][0] # 'COMPLETO'
            sale.save()
            # set_movement(total, payment_methods.type_method, customer, user)
    else:
        """Si el CLIETNE NO REGISTRA"""
        # set_movement(total, None, customer, user)


    sale.user_made = user
    sale.save()

    Payment.objects.create(
        user_made = user,
        amount = amount or total,
        payment_method = payment_methods,
        description = f"Pago de venta Nro: {sale.pk}",
        sale = sale,
    )


def set_movement(total, type_method, customer, user):
    description = "Venta de productos"
    if not 'Anonimo' in customer.first_name:
        description += " a %s" % customer.get_full_name()

    Movement.objects.create(
        user_made = user,
        payment_method = type_method,
        amount = total,
        cash_register = CashRegister.objects.filter(
            is_close = False,
            branch = user.branch,
            ).last(),
        description = description,
        currency = Currency.objects.first(),
        type_operation = "Ingreso",
    )


def process_service_order(request, customer):
    service_order = ServiceOrder(request.POST)
    correction_form = CorrectionForm(request.POST)
    material_form = MaterialForm(request.POST)
    color_form = ColorForm(request.POST)
    cristal_form = CristalForm(request.POST)
    tratamiento_form = TratamientForm(request.POST)
    pupilar_form = InterpupillaryForm(request.POST)

    if (
        correction_form.is_valid() and
        material_form.is_valid() and 
        color_form.is_valid() and
        cristal_form.is_valid() and 
        tratamiento_form.is_valid() and 
        pupilar_form.is_valid()
        ):

        # Create the main form instance
        ServiceOrder.objects.create_lab(
            request.user, service_order, correction_form, material_form,
            color_form, cristal_form, tratamiento_form, pupilar_form,
            customer
        )
        messages.success(request, 'Se ha registrado una nueva orden de servicio con exito.')
        return True # todo OK con el formulario
    else: 
        print(correction_form.errors)
    return False # hubo un error