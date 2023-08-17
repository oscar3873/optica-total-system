from django.urls import path
from .views import CustomerCreateView, HealthInsuranceCreateView

app_name = 'clients_app'

urlpatterns = [
    path(
        'new/customer/', 
        CustomerCreateView.as_view(),
        name='new_customer'
    ),
    path(
        'new/health_insurance/',  
        HealthInsuranceCreateView.as_view(),
        name='new_hi'
    ),
]
