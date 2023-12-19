from django import template

register = template.Library()

@register.filter
def custom_intcomma(value):
    # Primero, formateamos el número con comas para los miles y punto para los decimales
    formatted_number = f"{value:,.2f}"

    # Luego, reemplazamos las comas con puntos y el punto con una coma
    formatted_number = formatted_number.replace(",", "X").replace(".", ",").replace("X", ".")

    return formatted_number
