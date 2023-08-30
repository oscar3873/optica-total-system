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
        name='list'
    ),
    path(
        'detail/<pk>/',
        SupplierDetailView.as_view(),
        name='detail'
    ),
]
