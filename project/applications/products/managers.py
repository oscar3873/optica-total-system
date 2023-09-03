from applications.core.managers import BaseManager

class ProductManager(BaseManager):

    def get_features(self, product):
        intermed = product.product_feature.all()
        features = [item.feature for item in intermed]
        return features
    
    def all(self):
        return self.filter(deleted_at=None)
    
