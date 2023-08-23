from django.contrib import admin

from .models import Customer, MedicalHistory

# Register your models here.
admin.site.register(Customer)
admin.site.register(MedicalHistory)