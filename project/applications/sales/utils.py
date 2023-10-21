# Función para procesar un formulario individual
from decimal import Decimal

from .models import OrderDetail


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
    print(sum(sorted(lst)[:n]))
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