from django.urls import path
from .views import CustomerCreateView, HealthInsuranceCreateView

app_name = 'clients_app'

urlpatterns = [
    path(
        'new/', 
        CustomerCreateView.as_view(),
        name='new_customer'
    ),
    path(
        'health_insurance/new/',  
        HealthInsuranceCreateView.as_view(),
        name='new_hi'
    ),
]
