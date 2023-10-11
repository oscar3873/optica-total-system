from applications.core.managers import BaseManager

class ProductManager(BaseManager):

    def get_products_branch(self, branch):
        return self.filter(branch=branch, deleted_at=None)

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
    
    def get_feature_types_and_values(self, product):
        from .models import Feature

        intermedia = product.product_feature.all()
        
        features = list(set([row.feature.type.name for row in intermedia]))
        feature_data = {}


        for feature_name in features:
            feature_values = Feature.objects.filter(type__name=feature_name).values_list('value', flat=True)
            feature_data[feature_name] = feature_values
        
        return feature_data
    
class FeatureManager(BaseManager):
    pass

class FeatureTypeManager(BaseManager):
    pass