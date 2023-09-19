from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
#
from .views import *

app_name = 'sales_app'

urlpatterns = [
    path(
        'pos',
        PointOfSaleView.as_view(),
        name = 'point_of_sale_view'
    )
]