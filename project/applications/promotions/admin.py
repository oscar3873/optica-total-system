from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Promotion)
admin.site.register(PromotionProduct)
admin.site.register(TypePromotion)