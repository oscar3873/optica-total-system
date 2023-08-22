from django.db import models
#
from django.contrib.auth.models import BaseUserManager


class SupplierManager(BaseUserManager, models.Manager):

    def get_all_products(self, supplier):
        all = supplier.product_suppliers.all()
        return all
    