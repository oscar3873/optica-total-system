from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.

admin.site.register(Sale)
admin.site.register(OrderDetail)
# admin.site.register(PaymentMethod_Sale)
admin.site.register(Invoice)
admin.site.register(InvoiceType)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass
