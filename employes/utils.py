def obtener_nombres_de_campos(modelo, *campos_a_ignorar):
    """
    Obtiene los nombres (verbose name) de los campos de un modelo de Django, excluyendo los campos especificados.

    Parámetros:
    modelo (django.db.models.Model): El modelo del cual se quieren obtener los nombres (verbose name) de los campos.
    *campos_a_ignorar (str): Una lista variable de argumentos con los nombres de los campos a ignorar.

    Devuelve:
    list: Una lista de cadenas de texto con los nombres (verbose name) de los campos del modelo, excluyendo los campos especificados.

    Ejemplo:
    
    from miapp.models import CashRegister
    nombres_de_campos = obtener_nombres_de_campos(CashRegister, 'user_made', 'deleted_at')
    """
    campos_a_ignorar = list(campos_a_ignorar)
    
    # Obtén una lista de los nombres de todos los campos del modelo
    nombres_de_campos = [(field.name, field.verbose_name) for field in modelo._meta.fields if field.name not in campos_a_ignorar]
    
    # Filtra los campos que están en la lista de campos a ignorar
    nombres_de_campos_filtrados = [campo[1] for campo in nombres_de_campos]
    
    return nombres_de_campos

# Uso de la función
# from miapp.models import CashRegister
# nombres_de_campos = obtener_nombres_de_campos(CashRegister, 'user_made', 'deleted_at')
