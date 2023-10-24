# Función para procesar un formulario individual
from decimal import Decimal

from project.settings.base import DATE_NOW
from applications.cashregister.models import CashRegister, Currency, Movement, Transaction

from .models import*

def get_total_and_products(formset, all_products_to_sale):
    total = 0

    product = formset.cleaned_data['product']
    all_products_to_sale.append(product)
    quantity = formset.cleaned_data['quantity']
    for _ in range(quantity):
        total += product.sale_price
    return total

def process_formset(formset, promotional_products):
    if formset.is_valid():
        product = formset.cleaned_data['product']
        quantity = formset.cleaned_data['quantity']
        discount = formset.cleaned_data['discount'] or 0

        price = product.sale_price * Decimal((1 + discount/100))

        # order_detail = OrderDetail.objects.create(
        #     product=product, 
        #     quantity=quantity,
        #     price=price, 
        #     discount=discount)

        promotion = product.promotions.exists()
        if promotion:
            for _ in range(quantity):
                promotion = product.promotions.last().promotion
                promotional_products[promotion].append((product, discount))

        return None #order_detail

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

def switch_case(case, sale):
    if case == 'A':
        return sale.invoice.create( # CREA UN OBJ DE FACTURA
            # consultar Campos
        )
    elif case == 'B':
        return sale.receipt.create( # CREA UN OBJ DE RECIBO COMUN
            # consultar Campos
        )
    else:
        return None

def find_cristal_product(all_products_to_sale):
    for product in all_products_to_sale:
        if 'cristal' in product.category.name:
            return product
    return None

def generate_proof(proof_type): # generar factura o recibo
    pass

def process_customer(customer, sale, payment_methods, total, product_cristal):
    """
    Funcion que procesa los datos de metodos de pago y el tipo de cliente.
    """

    payment_total = 0
    for payment in payment_methods:
        payment.save(commit=False)
        payment_total += payment.amount
    
    if customer.has_credit_account:
        sale.state = Sale.STATE[1][0] # "PENDIENTE"
        # customer.credit_transactions.create(
        #     date = DATE_NOW,
        #     amount = sale.total,
        #     description = "Venta de productos"
        # )
        customer.credit_balance += sale.total
        # customer.save()
        if product_cristal:
            return True
    
    elif product_cristal: # 
        sale.state = Sale.STATE[1][0] # "PENDIENTE"
        sale.missing_balance = Decimal(total) - Decimal(payment_total)
        set_movement(payment_total, payment.type_method, customer)
        return True

    else:
        sale.state = Sale.STATE[0][0] # 'COMPLETO'
        sale.save()
        set_movement(total, payment.type_method, customer)
    # sale.save()


def set_movement(total, method, customer):
    Movement.objects.create(
        payment_method = method,
        amount = total,
        cash_register = CashRegister.objects.filter(
            is_closed = False,
            branch = customer.branch,
            ).last(),
        description = "Venta de productos a %s" % customer.get_full_name(),
        # currency = "Pesos",
        type_operation = "Ingreso",
    )