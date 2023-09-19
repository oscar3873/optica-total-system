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
        CalibrationOrderCreateView.as_view(), 
        name='laboratory_new'
    ),
    path(
        '<pk>/lab/new/',  # ASIGNA EL PEDIDO DE LAB POR CREAR AL CLIENTE EN EL QUE ESTÁ
        CalibrationOrderCreateView.as_view(), 
        name='laboratory_new'
    ),

    ####  UPDATE  ####
    path(
        '<pk>/update/', 
        CustomerUpdateView.as_view(),
        name='customer_update'
    ),
    path(
        '<pk_c>/lab/<pk>/update/',  # <pk_c>: para customer y poder volver a su detail (succes) <pk>: la clase UpdateView tomara como pk para matcheat con un objeto
        CalibrationOrderUpdateView.as_view(), 
        name='laboratory_update'
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

    #### LIST ####
    path(
        '',
        CustomerListView.as_view(),
        name='customer_view'
    ),
    path(
        'labs/',
        CalibrationOrderListView.as_view(),
        name='lab_view'
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
        CalibrationOrderDetailView.as_view(),
        name='laboratory_detail'
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
        CalibrationOrderDeleteView.as_view(),
        name='laboratory_delete'
    ),
    path(
        '<pk_c>/lab/<pk>/delete/',
        CalibrationOrderDeleteView.as_view(),
        name='laboratory_delete'
    ),

    path(
        'insurance/<pk>/delete/',
        HealthInsuranceDeleteView.as_view(),
        name='hi_delete'
    )
]
