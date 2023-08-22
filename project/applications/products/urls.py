from django.urls import path
from .views import *

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
    ),
    path(
        'new/feature/',
        FeatureCreateView.as_view(),
        name= 'new_feature'
    ),
    path(
        'new/feature_type/',
        FeatureTypeCreateView.as_view(),
        name= 'new_feature_type'
    ),
    # UPDATES

    path(
        'update/category/<pk>',
        CategoryUpdateView.as_view(),
        name='update_category'
    ),
    path(
        'update/brand/<pk>',
        BrandUpdateView.as_view(),
        name='update_brand'
    ),
    path(
        'update/product/<pk>',
        ProductUpdateView.as_view(),
        name='update_product'
    ),
    path(
        'update/feature/<pk>',
        FeatureUpdateView.as_view(),
        name= 'update_feature'
    ),
    path(
        'update/feature_type/<pk>/',
        FeatureTypeUpdateView.as_view(),
        name= 'update_feature_type'
    ),

    # LISTING

    path(
        'list/brands',
        BrandListView.as_view(),
        name= 'brand_list'
    ),
    path(
        'list/categories',
        CategoryListView.as_view(),
        name= 'category_list'
    ),
    path(
        'list/products',
        ProductListView.as_view(),
        name= 'product_list'
    ),

    # DETAILS

    path(
        'detail/<pk>',
        ProductListView.as_view(),
        name= 'detail'
    ),
]
