from django.contrib import admin

from .models import *
# Register your models here.

class PromotionAdmin(admin.ModelAdmin):
    list_display = ['name', 'type_prom', 'start_date', 'end_date', 'is_active']

admin.site.register(TypePromotion)
admin.site.register(Promotion, PromotionAdmin)
admin.site.register(PromotionProduct)

