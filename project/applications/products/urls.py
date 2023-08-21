from django.urls import path
from .views import CategoryCreateView, BrandCreateView, ProductCreateView

app_name = 'products_app'

urlpatterns = [
    path(
        'category/new/',
        CategoryCreateView.as_view(),
        name='new_category'
    ),
    path(
        'brand/new/',
        BrandCreateView.as_view(),
        name='new_brand'
    ),
    path(
        'product/new/',
        ProductCreateView.as_view(),
        name='new_product'
    )
]
