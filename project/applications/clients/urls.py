from django.urls import path
from .views import *

app_name = 'clients_app'

urlpatterns = [
    path(
        'new/customer/', 
        CustomerCreateView.as_view(),
        name='new_customer'
    ),
    path(
        'new/health_insurance/',  
        HealthInsuranceCreateView.as_view(),
        name='new_hi'
    ),
    path(
        'new/lab/',  
        CalibrationOrderCreateView.as_view(), 
        name='new_laboratory'
    ),
    ####  UPDATE  ####
    path(
        'update/customer/<pk>', 
        CustomerUpdateView.as_view(),
        name='update_customer'
    ),
    path(
        'update/lab/<pk>/',  
        CalibrationOrderUpdateView.as_view(), 
        name='update_laboratory'
    ),
    #### LIST ####
    path(
        'detail/<pk>/',
        CustomerDetailView.as_view(),
        name='detail'
    ),

    path(
        'list/customer',
        CustomerListView.as_view(),
        name='customer_list'
    ),
]
