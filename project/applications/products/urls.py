from django.urls import path
from .views import CategoryCreateView, BrandCreateView, ProductCreateView

app_name = 'products_app'

urlpatterns = [
    path(
        'new/category/',
        CategoryCreateView.as_view(),
        name='new_category'
    ),
    path(
        'new/brand/',
        BrandCreateView.as_view(),
        name='new_brand'
    ),
    path(
        'new/product/',
        ProductCreateView.as_view(),
        name='new_product'
    )
]
