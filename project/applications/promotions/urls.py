from django.urls import path

from .views import *

app_name = 'promotions_app'

urlpatterns = [
    path(
        'new/promotion/',
        PromotionCreateView.as_view(),
        name = 'promotion_new'
    ),
    path(
        'detail/promotion/<pk>',
        PromotionDetailView.as_view(),
        name = 'promotion_detail'
    ),

    path(
        'ajax_promotional_products',
        ajax_promotional_products,
        name = 'ajax_promotional_products'
    ),
    
    path(
        'update/promotion/<pk>',
        PromotionUpdateView.as_view(),
        name = 'promotion_update'
    ),
    
    path(
        'list',
        PromotionListView.as_view(),
        name = 'promotion_list'
    ),
    path(
        'delete/promotion/<pk>/',
        PromotionDeleteView.as_view(),
        name = 'promotion_delete'
    )
]