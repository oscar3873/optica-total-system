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