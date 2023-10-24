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
]