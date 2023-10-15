from django.urls import path

from .views import PromotionCreateView

app_name = 'promotions_app'

urlpatterns = [
    path(
        'new/promotion',
        PromotionCreateView.as_view(),
        name='new_promotion'
    ),
]