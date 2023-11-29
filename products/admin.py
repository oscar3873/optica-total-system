from django.contrib import admin

from .models import *
# Register your models here.

class GenericAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',  # Mostrar el nombre del producto en la lista del admin
        'updated_at',  # Mostrar la fecha de actualización
    ]

class FeatureAdmin(admin.ModelAdmin):
    list_display = [
        'value',  # Mostrar el nombre del producto en la lista del admin
        'updated_at',  # Mostrar la fecha de actualización
    ]

admin.site.register(Product, GenericAdmin)
admin.site.register(Category, GenericAdmin)
admin.site.register(Brand, GenericAdmin)
admin.site.register(Feature_type, GenericAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Product_feature)
# admin.site.register(Discount_Product)