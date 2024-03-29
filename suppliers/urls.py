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

    path(
        'detail/<pk_s>/bank/update/<pk>/',
        BankUpdateView.as_view(),
        name='bank_update'
    ),
    
    ### AJAX PARA CREAR BANCO PARA SUPPLIER
    path(
        'ajax-bank-supplier/',
        set_bank_supplier,
        name='set_bank_supplier'
    ),
    
    path(
        'brands/ajax-search-brands/', 
        ajax_search_brands, 
        name='ajax_search_brands'
    ),

    path(
        'ajax-new-bank/',
        ajax_new_bank,
        name='ajax_new_bank'
    ),

    path(
        'ajax-delete-bank/<pk>/',
        ajax_delete_bank,
        name='ajax_delete_bank'
    )
]
