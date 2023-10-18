from django.urls import path

from .views import PromotionCreateView, PromotionDetailView

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
]