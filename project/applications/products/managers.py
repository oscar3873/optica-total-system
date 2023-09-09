from applications.core.managers import BaseManager

from . import models
class ProductManager(BaseManager):

    def get_features(self, product):
        """
        Obtiene todas caractefristicas relacionadas a un producto (argumento)
        """
        try:
            #Trato de obtener las caracteristicas relacionada a un producto si es que ese producto existe
            intermed = product.product_feature.all()
            features = [item.feature for item in intermed]
        except:
            features = None
        return features
    
    
    def all(self):
        return self.filter(deleted_at=None)
    

class ProductFeatureManager(BaseManager):
    def form_in_out_features(self, form, product, user):
        """
        PARA FORMULARIOS:
            Verifica el estado de las caracteristicas cargadas para el producto.
            En caso de requerir poner/sacar caracteristicas de un producto.
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

    def form_create_features_formset(self, product, feature_formset):
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
                type, created = models.Feature_type.objects.get_or_create(
                                    user_made=self.request.user,
                                    name=feature_type_name)
                value, created = models.Feature.objects.get_or_create(
                                    user_made=self.request.user,
                                    type=type,
                                    value=feature_value
                                )
                feature_dict[value] = type

        for feature, feature_type_name in feature_dict.items():
            intermedia, created = self.model.objects.get_or_create(
                product=product,
                feature=feature
            )
            if created:
                intermedia.user_made = self.request.user
                intermedia.save()