from django.urls import path

from .views import PromotionCreateView

app_name = 'promotions_app'

urlpatterns = [
    path(
        'new/combo',
        PromotionCreateView.as_view(),
        name = 'promotion_new'
    ),
]