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

    ########## PROMOTIONS ##########
    path(
        'promotions/new',
        PromotionCreateView.as_view(),
        name = 'promotion_new'
    ),
]