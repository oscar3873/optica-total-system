from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.

admin.site.register(Sale)
admin.site.register(OrderDetaill)
admin.site.register(PaymentMethod_Sale)
admin.site.register(Invoice)
admin.site.register(PaymentMethod)