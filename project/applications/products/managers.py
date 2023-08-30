from django.db import models
from django.contrib.auth.models import BaseUserManager

class ProductManager(BaseUserManager, models.Manager):

    def get_features(self, product):
        intermed = product.product_feature.all()
        features = [item.feature for item in intermed]
        return features
    
    
