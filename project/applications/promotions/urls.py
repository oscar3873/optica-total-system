from django.urls import path

from .views import *

app_name = 'promotions_app'

urlpatterns = [
    path(
        'new/combo',
        PromotionCreateView.as_view(),
        name = 'promotion_new'
    ),
    path(
        'detail',
        PromotionDetailView.as_view(),
        name = 'promotion_detail'
    ),

    path(
        'ajax_promotional_products',
        ajax_promotional_products,
        name = 'ajax_promotional_products'
    ),
    
    path(
        'update',
        PromotionUpdateView.as_view(),
        name = 'promotion_update'
    ),
    
    path(
        'list',
        PromotionListView.as_view(),
        name = 'promotion_list'
    ),
    path(
        'delete',
        PromotionDeleteView.as_view(),
        name = 'promotion_delete'
    )
]