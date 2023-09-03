from applications.core.managers import BaseManager

class ProductManager(BaseManager):

    def get_features(self, product):
        intermed = product.product_feature.all()
        features = [item.feature for item in intermed]
        return features
    
    def all(self):
        return self.filter(deleted_at=None)
    

class ProductFeatureManager(BaseManager):
    def IO_features_form(self, form, product, user):
        """
        PARA FORMULARIOS:
            Verifica el estado de las caracteristicas cargadas para el producto
            En caso de requerir poner/sacar caracteristicas de un producto
        """
        selected_features = form.cleaned_data['features']
        existing_features = product.product_feature.all()

        # Elimina relaciones existentes que ya no están seleccionadas
        for feature in existing_features:
            if feature.feature not in selected_features:
                product.product_feature.get(feature=feature.feature).delete()

        # Crea nuevas relaciones solo para características no existentes
        for feature in selected_features:
            if feature not in existing_features.values_list('feature', flat=True):
                product.product_feature.create(feature=feature, user_made=user)

    def create_features_to_products(self, product, feature_formset):
        feature_dict = {}

        for feature_form in feature_formset:
            feature_type_name = feature_form.cleaned_data.get('type', '').strip().lower()
            feature_value = feature_form.cleaned_data.get('value', '').strip().lower()

            if feature_type_name and feature_value:
                # Create FeatureType if it doesn't exist
                feature_type, created = Feature_type.objects.get_or_create(
                                            user_made=self.request.user,
                                            name=feature_type_name)
                value, created = Feature.objects.get_or_create(
                                    user_made=self.request.user,
                                    type=feature_type,
                                    value=feature_value
                                )
                feature_dict[value] = feature_type

        for feature, feature_type_name in feature_dict.items():
            intermedia, created = self.model.objects.get_or_create(
                product=product,
                feature=feature
            )
            if created:
                intermedia.user_made = self.request.user
                intermedia.save()