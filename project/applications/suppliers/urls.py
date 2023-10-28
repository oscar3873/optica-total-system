from django.urls import path
from .views import *

app_name = 'suppliers_app'

urlpatterns = [
    path(
        'new/',
        SupplierCreateView.as_view(),
        name='new_supplier'
    ),
    path(
        'update/<pk>/',
        SupplierUpdateView.as_view(),
        name='update_supplier'
    ),
    path(
        'list/',
        SuppliersListView.as_view(),
        name='list_supplier'
    ),
    path(
        'detail/<pk>/',
        SupplierDetailView.as_view(),
        name='supplier_detail'
    ),
    path(
        'delete/<pk>/',
        SupplierDeleteView.as_view(),
        name='supplier_delete'
    ),
    
    ### AJAX PARA CREAR BANCO PARA SUPPLIER
    path(
        'ajax_bank_supplier',
        set_bank_supplier,
        name='set_bank_supplier'
    ),
    
    path(
        'brands/ajax_search_brands/', 
        ajax_search_brands, 
        name='ajax_search_brands'),

]
