from django.urls import path
from .views import *

app_name = 'clients_app'

urlpatterns = [
    path(
        'new/', 
        CustomerCreateView.as_view(),
        name='customer_new'
    ),
    path(
        'health_insurance/new/', # PARA REGISTRAR OBRAS SOCIALES
        HealthInsuranceCreateView.as_view(),
        name='hi_new'
    ),
    path(
        '<pk>/service_order/new/',  # ASIGNA EL PEDIDO DE LAB POR CREAR AL CLIENTE EN EL QUE ESTÁ
        ServiceOrderCreateView.as_view(), 
        name='service_order_new'
    ),

    ####  UPDATE  ####
    path(
        'update/<pk>/', 
        CustomerUpdateView.as_view(),
        name='customer_update'
    ),
    path(
        'service_order/update/<pk>',  # <pk_c>: para customer y poder volver a su detail (succes) <pk>: la clase UpdateView tomara como pk para matcheat con un objeto
        ServiceOrderUpdateView.as_view(), 
        name='service_order_update'
    ),
    path(
        'health_insurance/update/<pk>',
        HealthInsuranceUpdateView.as_view(), 
        name='insurance_update'
    ),

    #### LIST ####
    path(
        '',
        CustomerListView.as_view(),
        name='customer_view'
    ),
    path(
        'service_orders/',
        ServiceOrderListView.as_view(),
        name='service_order_view'
    ),
    path(
        'health_insurances/',
        HealthInsuranceListView.as_view(),
        name='insurance_view'
    ),

    ####### DETAIL #######
    path(
        'detail/<pk>',
        CustomerDetailView.as_view(),
        name='customer_detail'
    ),
    path(
        'service_order/detail/<pk>', # <pk_c>: para customer y poder volver a su detail (succes) <pk>: la clase DetailView tomara como pk para matcheat con un objeto
        ServiceOrderDetailView.as_view(),
        name='service_order_detail'
    ),
    path(
        'insurance/detail/<pk>',
        HealthInsuranceDetailView.as_view(),
        name='hi_detail'
    ),

    ######### DELETE ##########
    path(
        'delete/<pk>',
        CustomerDeleteView.as_view(),
        name='customer_delete'
    ),
    path(
        'service_order/delete/<pk>',
        ServiceOrderDeleteView.as_view(),
        name='service_order_delete'
    ),
    path(
        'insurance/delete/<pk>',
        HealthInsuranceDeleteView.as_view(),
        name='hi_delete'
    ),

    ########## SERVICE ORDER OF CUSTOMER EXCEL ##########
    path(
        'detail/<pk>/export_service_orders',
        export_order_service_list_to_excel,
        name='export_service_orders'
    ),

    ########### OPEN CREDIT ACCOUNT ############
    path(
        'open_credit_account/<pk>',
        open_credit_account,
        name='open_credit_account'
    ),

    ########### CLOSE CREDIT ACCOUNT ############
    path(
        'close_credit_account/<pk>',
        close_credit_account,
        name='close_credit_account'
    ),

    ########## PAY CREDITS EXCEL #########
    path(
        'pay_credits/<pk>',
        pay_credits,
        name='pay_credits'
    ),

    ########## CUSTOMER LIST EXCEL ##########
    path(
        'export_customer_list',
        export_customer_list_to_excel,
        name='export_customer_list'
    ),
]