from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
#
from applications.cashregister.views import *

app_name = 'cashregister_app'

urlpatterns = [
    path(
        '',
        CashRegisterView.as_view(),
        name = 'cashregister_view'
    ),
    path(
        'list/',
        CashRegisterListView.as_view(),
        name = 'cashregister_list_view'
    ),
    path(
        'detail/<pk>',
        CashRegisterDetailView.as_view(),
        name = 'cashregister_detail_view'
    ),
    path(
        'update/<pk>',
        CashRegisterUpdateView.as_view(),
        name = 'cashregister_update_view'
    ),
    path(
        'delete/<pk>',
        CashRegisterDeleteView.as_view(),
        name = 'cashregister_delete_view'
    ),
    path(
        'create/',
        CashRegisterCreateView.as_view(),
        name = 'cashregister_create_view'
    ),
    path(
        'arching/',
        CashRegisterArching.as_view(),
        name = 'cashregister_arching_view'
    ),
    path(
        'close/',
        CashRegisterArching.as_view(),
        name = 'cashregister_close_view'
    ),
    path(
        'movements/',
        MovementsView.as_view(),
        name = 'movements_view'
    ),
    path(
        'movements/detail/<pk>',
        MovementsDetailView.as_view(),
        name = 'movements_detail_view'
    ),
    path(
        'movements/create',
        MovementsCreateView.as_view(),
        name = 'movements_create_view'
    ),
    path(
        'movements/update/<pk>',
        MovementsUpdateView.as_view(),
        name = 'movements_update_view'
    ),
    path(
        'movements/delete/<pk>',
        MovementsDeleteView.as_view(),
        name = 'movements_delete_view'
    ),
        ########## SEARCH PRODUCTS LIST #########
    path(
        'ajax_search_products/',
        ajax_search_movements,
        name='ajax_search_movements'
    ),
    path(
        'currency/create',
        CurrencyCreateView.as_view(),
        name = 'currency_create_view'
    ),
    path(
        'currency/',
        CurrencyView.as_view(),
        name = 'currency_view'
    ),
]
