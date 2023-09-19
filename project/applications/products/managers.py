from applications.core.managers import BaseManager

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
    
class FeatureManager(BaseManager):
    pass

class FeatureTypeManager(BaseManager):
    pass