from django.urls import path
from .views import *

app_name = 'suppliers_app'

urlpatterns = [
    path(
        'new/',
        SupplierCreateView.as_view(),
        name='new_supplier'
    ),
]
