from applications.core.managers import BaseManager

from . import models
class ProductManager(BaseManager):

    def get_features(self, product):
        """
        Obtiene todas caractefristicas relacionadas a un producto (argumento)
        """
        intermed = product.product_feature.all()
        features = [item.feature for item in intermed]
        return features
    
    def all(self):
        return self.filter(deleted_at=None)
    