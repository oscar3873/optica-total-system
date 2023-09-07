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
        'close/',
        CashRegisterClosedView.as_view(),
        name = 'cashregister_close_view'
    ),
    path(
        'movements/',
        MovementsView.as_view(),
        name = 'movements_view'
    ),
    path(
        'movements/create',
        MovementsCreateView.as_view(),
        name = 'movements_create_view'
    ),
    path(
        'movements/delete/<pk>',
        MovementsDeleteView.as_view(),
        name = 'movements_delete_view'
    ),
    path(
        'closed',
        MovementsClosedView.as_view(),
        name = 'cashregister_closed'
    ),
]
