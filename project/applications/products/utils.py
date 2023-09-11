from .models import Feature, Feature_type, Product_feature

"""Poner la funcion en core
"""


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
    print(nombres_de_campos)
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
# print(nombres_de_campos)





def form_in_out_features(form, product, user):
        """
        PARA FORMULARIOS:
            Verifica el estado de las caracteristicas cargadas para el producto.
            En caso de requerir poner/sacar caracteristicas de un producto.
        """
        selected_features = form.cleaned_data['features']
        existing_features = product.product_feature.all()

        # Elimina relaciones existentes que ya no están seleccionadas
        for intermedia in existing_features:
            if intermedia.feature not in selected_features:
                product.product_feature.get(feature=intermedia.feature).delete()

        # Crea nuevas relaciones solo para características no existentes
        for feature in selected_features:
            if feature not in existing_features.values_list('feature', flat=True):
                intermedia, created = product.product_feature.get_or_create(feature=feature)
                if created:
                    intermedia.user_made = user
                    intermedia.save()


def form_create_features_formset(user, product, feature_formset):
        """
        PARA FORMULARIOS:
            Obtiene o crea las caracteristicas para relacionarlo con el producto (mediante tabla interemedia).
        """
        feature_dict = {}

        for feature_form in feature_formset:
            feature_type_name = feature_form.cleaned_data.get('type', '').strip().lower()
            feature_value = feature_form.cleaned_data.get('value', '').strip().lower()

            if feature_type_name and feature_value:
                # Create FeatureType if it doesn't exist
                type, created_type = Feature_type.objects.get_or_create(
                                    user_made=user,
                                    name=feature_type_name)
                value, created_value = Feature.objects.get_or_create(
                                    user_made=user,
                                    type=type,
                                    value=feature_value
                                )
                feature_dict[value] = type

        for feature, feature_type in feature_dict.items():
            intermedia, created = product.product_feature.get_or_create(feature=feature)
            if created:
                intermedia.user_made = user
                intermedia.save()