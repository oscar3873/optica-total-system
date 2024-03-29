from django.urls import path
from .views import *

app_name = 'products_app'

urlpatterns = [
    ########### CREATE
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
        'new/feature-type/',
        FeatureTypeCreateView.as_view(),
        name= 'new_feature_type'
    ),
    path(
        'new/feature_full/',
        FeatureFullCreateView.as_view(),
        name= 'new_feature_type'
    ),
    path(
        'new/feature-unit/',
        FeatureUnitCreateView.as_view(),
    ),
    ############### UPDATES

    path(
        'update/category/<pk>/',
        CategoryUpdateView.as_view(),
        name='update_category'
    ),
    path(
        'update/brand/<pk>/',
        BrandUpdateView.as_view(),
        name='update_brand'
    ),
    path(
        'update/product/<pk>/',
        ProductUpdateView.as_view(),
        name='update_product'
    ),
    path(
        'update/feature/<pk>/',
        FeatureUpdateView.as_view(),
        name= 'update_feature'
    ),
    path(
        'update/feature-type/<pk>/',
        FeatureTypeUpdateView.as_view(),
        name= 'update_feature_type'
    ),

    ############### LISTING

    path(
        'list/brand',
        BrandListView.as_view(),
        name= 'brand_list'
    ),
    path(
        'list/category',
        CategoryListView.as_view(),
        name= 'category_list'
    ),
    path(
        'list/product',
        ProductListView.as_view(),
        name= 'product_list'
    ),
    path(
        'list/feature/',
        FeatureListView.as_view(),
        name= 'feature_list'
    ),
    path(
        'list/feature-type/',
        FeatureTypeListView.as_view(),
        name= 'homefeature_type_list'
    ),

    ############## DETAILS

    path(
        'detail/product/<pk>/',
        ProductDetailView.as_view(),
        name= 'product_detail'
    ),

    path(
        'detail/category/<pk>/',
        CategoryDetailView.as_view(),
        name= 'category_detail'
    ),

    path(
        'detail/brand/<pk>/',
        BrandDetailView.as_view(),
        name= 'brand_detail'
    ),

    ################# DELETE
    path(
        'delete/product/<pk>/',
        ProductDeleteView.as_view(),
        name='product_delete'
    ),
    path(
        'delete/category/<pk>/',
        CategoryDeleteView.as_view(),
        name='category_delete'
    ),
    path(
        'delete/brand/<pk>/',
        BrandDeleteView.as_view(),
        name='brand_delete'
    ),

    ################ SEARCH
    #path(
    #    'search/',
    #    ProductSearchView.as_view(),
    #    name='product_search'
    #),

    ################# actualizacion de precio
    path(
        'update-price/', 
        UpdatePriceView.as_view(), 
        name='update_price_advanced'
    ),
    path(
        'search-categories-or-brands/', 
        search_categories_or_brands, 
        name='search_categories_or_brands'
    ), 

    ######### EXPORT TO EXCEL ##########
    path(
        'export_list_products/', 
        export_products_list_to_excel, 
        name='export_list_products'
    ), 

    ########## SEARCH PRODUCTS LIST #########
    path(
        'ajax-search-products/',
        ajax_search_products,
        name='ajax_search_products'
    ),
    
    path(
        'ajax-search-products-promotion/',
        ajax_search_products_promotion,
        name='ajax_search_products_promotion'
    )
]
