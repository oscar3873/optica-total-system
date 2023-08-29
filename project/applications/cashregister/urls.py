from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
#
from applications.cashregister.views import *

app_name = 'cashregister_app'

urlpatterns = [
    path(
        'create/',
        CashRegisterCreateView.as_view(),
        name = 'cashregister_create'
    ),
    path(
        '',
        CashRegisterView.as_view(),
        name = 'cashregister_view'
    ),
    path(
        'movements',
        MovementsView.as_view(),
        name = 'movements_view'
    ),
    path(
        'closed',
        MovementsClosedView.as_view(),
        name = 'cashregister_closed'
    ),
]
