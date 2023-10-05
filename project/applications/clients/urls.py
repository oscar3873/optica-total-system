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
        '<pk>/health_insurance/new/', # PARA REGISTRAR UNA OBRAS SOCIAL A EL CLIENTE
        HealthInsuranceCreateView.as_view(),
        name='hi_new'
    ),
    path(
        'lab/new/',  # PARA CREAR PERDIDO DE LAB "FANTASMA" (SIN CLIENTE)
        ServiceOrderCreateView.as_view(), 
        name='only_service_order_new'
    ),
    path(
        '<pk>/lab/new/',  # ASIGNA EL PEDIDO DE LAB POR CREAR AL CLIENTE EN EL QUE ESTÁ
        ServiceOrderCreateView.as_view(), 
        name='service_order_new'
    ),

    ####  UPDATE  ####
    path(
        '<pk>/update/', 
        CustomerUpdateView.as_view(),
        name='customer_update'
    ),
    path(
        '<pk_c>/lab/<pk>/update/',  # <pk_c>: para customer y poder volver a su detail (succes) <pk>: la clase UpdateView tomara como pk para matcheat con un objeto
        ServiceOrderUpdateView.as_view(), 
        name='service_order_update'
    ),
    path(
        '<pk_c>/health_insurance/<pk>/update/', # <pk_c>: para customer y poder volver a su detail (succes) <pk>: la clase UpdateView tomara como pk para matcheat con un objeto
        HealthInsuranceUpdateView.as_view(), 
        name='insurance_update'
    ),
    path(
        'health_insurance/<pk>/update/', # <pk_c>: para customer y poder volver a su detail (succes) <pk>: la clase UpdateView tomara como pk para matcheat con un objeto
        HealthInsuranceUpdateView.as_view(), 
        name='insurance_update'
    ),
    path(
        '<pk>/update_for_employees',
        CustomerUpdateHealthInsurance.as_view(),
        name='customer_update_for_employees'
    ),

    #### LIST ####
    path(
        '',
        CustomerListView.as_view(),
        name='customer_view'
    ),
    path(
        'labs/',
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
        '<pk>/',
        CustomerDetailView.as_view(),
        name='customer_detail'
    ),
    path(
        '<pk_c>/lab/<pk>/detail/', # <pk_c>: para customer y poder volver a su detail (succes) <pk>: la clase DetailView tomara como pk para matcheat con un objeto
        ServiceOrderDetailView.as_view(),
        name='service_order_detail'
    ),
    path(
        'insurance/<pk>/detail/',
        HealthInsuranceDetailView.as_view(),
        name='hi_detail'
    ),

    ######### DELETE ##########
    path(
        '<pk>/delete/',
        CustomerDeleteView.as_view(),
        name='customer_delete'
    ),
    path(
        'lab/<pk>/delete/',
        ServiceOrderDeleteView.as_view(),
        name='service_order_delete'
    ),
    path(
        '<pk_c>/lab/<pk>/delete/',
        ServiceOrderDeleteView.as_view(),
        name='service_order_delete'
    ),

    path(
        'insurance/<pk>/delete/',
        HealthInsuranceDeleteView.as_view(),
        name='hi_delete'
    ),

    ########## EXCEL ##########
    path(
        '<pk>/export',
        export_order_service_list_to_excel,
        name='export_service_orders'
    )
]