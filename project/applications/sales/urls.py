from django.urls import path
#
from .views import *

app_name = 'sales_app'

urlpatterns = [
    path(
        'pos/',
        PointOfSaleView.as_view(),
        name = 'point_of_sale_view'
    ),
    path(
        'payment-method/create',
        PaymentMethodCreateView.as_view(),
        name = 'payment_method_create_view'
    ),
    path(
        'currency/',
        PaymentMethodView.as_view(),
        name = 'payment_method_view'
    ),
    path(
        'list/',
        SalesListView.as_view(),
        name = 'sales_list_view'
    ),
    path(
        'detail/<pk>/',
        SaleDetailView.as_view(),
        name = 'sale_detail_view'
    ),
    path(
        'ajax-search-sales/',
        ajax_search_sales,
        name='ajax_search_sales'
    ),

    ######## MUESTRA TICKET DE VENTA Y ORDEN DE SERVICIO EN CASO DE HABER ########
    path(
        'show-invoice/<pk>/',
        show_invoice,
        name='show_invoice'
    ),
    
    path(
        'show-factura/<pk>/',
        show_factura,
        name='show_factura'
    ),

    ######## ORDEN DE SERVICIO EN DETALLE DE VENTA ########
    path(
        'order-service/<pk>/',
        set_serviceOrder_onSale,
        name='order_service'
    ),

    ########### IMPRIMIR FACTURA #########
    path(
        'print-invoice/<pk>/',
        print_invoice,
        name='print_invoice'
    ),

    ########### PAGAR DEUDA ACUMULADA DE UNA VENTA #########
    path(
        'pay-missing-balance/<pk>/',
        pay_missing_balance,
        name='pay_missing_balance'
    )
]