from django.contrib import admin

from .models import Customer, Material

# Register your models here.
admin.site.register(Customer)
admin.site.register(Material)