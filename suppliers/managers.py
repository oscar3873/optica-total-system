from core.managers import BaseManager

class SupplierManager(BaseManager):

    def get_all_products(self, supplier):
        all = supplier.product_suppliers.all()
        return all
    
    def all(self):
        return self.filter(deleted_at=None)